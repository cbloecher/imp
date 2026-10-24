import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas, service
from .db import get_db

router = APIRouter(prefix="/api")


@router.get("/lookups", response_model=schemas.LookupsOut)
def list_lookups(db: Session = Depends(get_db)):
    result = {}
    for kind, model in service.LOOKUP_MODELS.items():
        result[kind] = list(
            db.scalars(select(model).where(model.archived.is_(False)).order_by(model.name)).all()
        )
    return result


@router.post("/lookups/{kind}", response_model=schemas.LookupOut, status_code=201)
def create_lookup(kind: str, payload: schemas.LookupCreate, db: Session = Depends(get_db)):
    model = service.LOOKUP_MODELS.get(kind)
    if model is None:
        raise HTTPException(404, "Unknown lookup kind")
    row = model(name=payload.name.strip(), slug=service.unique_slug(db, model, payload.name))
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.patch("/lookups/{kind}/{lookup_id}", response_model=schemas.LookupOut)
def rename_lookup(kind: str, lookup_id: uuid.UUID, payload: schemas.LookupUpdate, db: Session = Depends(get_db)):
    model = service.LOOKUP_MODELS.get(kind)
    if model is None:
        raise HTTPException(404, "Unknown lookup kind")
    row = db.get(model, lookup_id)
    if row is None:
        raise HTTPException(404, "Lookup not found")
    row.name = payload.name.strip()
    db.commit()
    db.refresh(row)
    return row


@router.get("/tree", response_model=list[schemas.TreeNode])
def tree(db: Session = Depends(get_db)):
    return service.build_tree(db)


@router.get("/items", response_model=list[schemas.ItemOut])
def list_items(
    organisation_id: uuid.UUID | None = None,
    function_id: uuid.UUID | None = None,
    topic_id: uuid.UUID | None = None,
    tag_id: uuid.UUID | None = None,
    state: str | None = None,
    inbox: bool = False,
    sprint: bool = False,
    has_review: bool = False,
    delegated: bool = False,
    db: Session = Depends(get_db),
):
    stmt = service.item_query().order_by(models.Item.updated_at.desc())

    if organisation_id:
        stmt = stmt.where(models.Item.organisations.any(models.Organisation.id == organisation_id))
    if function_id:
        stmt = stmt.where(models.Item.functions.any(models.WorkFunction.id == function_id))
    if topic_id:
        stmt = stmt.where(models.Item.topics.any(models.Topic.id == topic_id))
    if tag_id:
        stmt = stmt.where(models.Item.tags.any(models.Tag.id == tag_id))
    if state:
        stmt = stmt.where(models.Item.state == state)
    if inbox:
        stmt = stmt.where(
            ~models.Item.organisations.any(),
            ~models.Item.functions.any(),
            ~models.Item.topics.any(),
        )
    if has_review:
        stmt = stmt.where(models.Item.review_after.is_not(None))
    if delegated:
        stmt = stmt.where(models.Item.delegated_to.is_not(None))

    items = list(db.scalars(stmt).unique().all())
    memberships = service.sprint_membership_map(db, [item.id for item in items])
    if sprint:
        items = [item for item in items if item.id in memberships]
    return [service.serialize_item(item, memberships.get(item.id)) for item in items]


@router.get("/items/{item_id}", response_model=schemas.ItemOut)
def get_item(item_id: uuid.UUID, db: Session = Depends(get_db)):
    item = db.scalar(service.item_query().where(models.Item.id == item_id))
    if item is None:
        raise HTTPException(404, "Item not found")
    memberships = service.sprint_membership_map(db, [item.id])
    return service.serialize_item(item, memberships.get(item.id))


@router.post("/items", response_model=schemas.ItemOut, status_code=201)
def create_item(payload: schemas.ItemCreate, db: Session = Depends(get_db)):
    item = models.Item(
        title=payload.title.strip(),
        description=payload.description,
        type=payload.type,
        state=payload.state,
        due_at=payload.due_at,
        review_after=payload.review_after,
        delegated_to=payload.delegated_to,
        waiting_for=payload.waiting_for,
    )
    try:
        item.organisations = service.get_lookups(db, "organisations", payload.organisation_ids)
        item.functions = service.get_lookups(db, "functions", payload.function_ids)
        item.topics = service.get_lookups(db, "topics", payload.topic_ids)
        item.tags = service.get_lookups(db, "tags", payload.tag_ids)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    db.add(item)
    db.commit()
    item = db.scalar(service.item_query().where(models.Item.id == item.id))
    return service.serialize_item(item)


@router.patch("/items/{item_id}", response_model=schemas.ItemOut)
def update_item(item_id: uuid.UUID, payload: schemas.ItemUpdate, db: Session = Depends(get_db)):
    item = db.scalar(service.item_query().where(models.Item.id == item_id))
    if item is None:
        raise HTTPException(404, "Item not found")

    fields = payload.model_fields_set
    for field in ["title", "description", "type", "state", "due_at", "review_after", "delegated_to", "waiting_for"]:
        if field in fields:
            value = getattr(payload, field)
            if field == "title":
                if value is None:
                    raise HTTPException(400, "title cannot be null")
                value = value.strip()
            setattr(item, field, value)

    lookup_fields = {
        "organisation_ids": ("organisations", "organisations"),
        "function_ids": ("functions", "functions"),
        "topic_ids": ("topics", "topics"),
        "tag_ids": ("tags", "tags"),
    }
    try:
        for payload_field, (attribute, kind) in lookup_fields.items():
            if payload_field in fields:
                setattr(item, attribute, service.get_lookups(db, kind, getattr(payload, payload_field) or []))
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc

    db.commit()
    item = db.scalar(service.item_query().where(models.Item.id == item.id))
    membership = service.sprint_membership_map(db, [item.id]).get(item.id)
    return service.serialize_item(item, membership)


@router.put("/items/{item_id}/sprint", response_model=schemas.ItemOut)
def toggle_sprint(item_id: uuid.UUID, payload: schemas.SprintToggle, db: Session = Depends(get_db)):
    item = db.scalar(service.item_query().where(models.Item.id == item_id))
    if item is None:
        raise HTTPException(404, "Item not found")

    sprint = service.get_or_create_current_sprint(db)
    membership = db.scalar(
        select(models.SprintItem).where(
            models.SprintItem.sprint_id == sprint.id,
            models.SprintItem.item_id == item.id,
        )
    )
    if payload.included:
        if membership is None:
            membership = models.SprintItem(
                sprint_id=sprint.id,
                item_id=item.id,
                kind=payload.kind,
            )
            db.add(membership)
        else:
            membership.kind = payload.kind
    elif membership is not None:
        db.delete(membership)

    db.commit()
    kind = payload.kind if payload.included else None
    return service.serialize_item(item, kind)
