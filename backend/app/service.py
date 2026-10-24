import uuid
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from slugify import slugify

from . import models


LOOKUP_MODELS = {
    "organisations": models.Organisation,
    "functions": models.WorkFunction,
    "topics": models.Topic,
    "tags": models.Tag,
}


def item_query():
    return select(models.Item).options(
        selectinload(models.Item.organisations),
        selectinload(models.Item.functions),
        selectinload(models.Item.topics),
        selectinload(models.Item.tags),
        selectinload(models.Item.source_object).selectinload(models.SourceObject.source),
    )


def unique_slug(db: Session, model, name: str) -> str:
    base = slugify(name) or "item"
    candidate = base
    suffix = 2
    while db.scalar(select(model.id).where(model.slug == candidate)):
        candidate = f"{base}-{suffix}"
        suffix += 1
    return candidate


def get_lookups(db: Session, kind: str, ids: list[uuid.UUID]):
    model = LOOKUP_MODELS[kind]
    if not ids:
        return []
    rows = list(db.scalars(select(model).where(model.id.in_(ids), model.archived.is_(False))).all())
    if len(rows) != len(set(ids)):
        raise ValueError(f"Unknown {kind} id")
    return rows


def get_or_create_current_sprint(db: Session) -> models.Sprint:
    today = date.today()
    sprint = db.scalar(select(models.Sprint).where(models.Sprint.date == today, models.Sprint.state == "open"))
    if sprint is None:
        sprint = models.Sprint(date=today, state="open")
        db.add(sprint)
        db.flush()
    return sprint


def sprint_membership_map(db: Session, item_ids: list[uuid.UUID]) -> dict[uuid.UUID, str]:
    if not item_ids:
        return {}
    sprint = db.scalar(select(models.Sprint).where(models.Sprint.date == date.today(), models.Sprint.state == "open"))
    if sprint is None:
        return {}
    rows = db.execute(
        select(models.SprintItem.item_id, models.SprintItem.kind).where(
            models.SprintItem.sprint_id == sprint.id,
            models.SprintItem.item_id.in_(item_ids),
        )
    ).all()
    return {row.item_id: row.kind for row in rows}


def serialize_item(item: models.Item, sprint_kind: str | None = None) -> dict:
    source = None
    if item.source_object and item.source_object.source:
        source = {
            "source_type": item.source_object.source.type,
            "source_name": item.source_object.source.name,
            "external_id": item.source_object.external_id,
            "external_url": item.source_object.external_url,
            "source_state": item.source_object.source_state,
        }
    return {
        "id": item.id,
        "title": item.title,
        "description": item.description,
        "type": item.type,
        "state": item.state,
        "due_at": item.due_at,
        "review_after": item.review_after,
        "delegated_to": item.delegated_to,
        "waiting_for": item.waiting_for,
        "organisations": item.organisations,
        "functions": item.functions,
        "topics": item.topics,
        "tags": item.tags,
        "source": source,
        "in_current_sprint": sprint_kind is not None,
        "sprint_kind": sprint_kind,
        "created_at": item.created_at,
        "updated_at": item.updated_at,
    }


def build_tree(db: Session) -> list[dict]:
    items = list(
        db.scalars(
            item_query().where(models.Item.state.not_in(["done", "cancelled", "archived"]))
        ).unique().all()
    )

    def ids_for(values):
        return {str(v.id) for v in values}

    inbox_count = sum(
        1 for item in items if not item.organisations and not item.functions and not item.topics
    )
    root = {
        "id": "person:self",
        "text": "Ich",
        "kind": "person",
        "count": len(items),
        "filters": {},
        "children": [
            {
                "id": "view:inbox",
                "text": "Inbox / ungeordnet",
                "kind": "view",
                "count": inbox_count,
                "filters": {"inbox": True},
                "children": [],
            }
        ],
    }

    organisations = list(
        db.scalars(select(models.Organisation).where(models.Organisation.archived.is_(False)).order_by(models.Organisation.name))
    )
    for org in organisations:
        org_items = [item for item in items if str(org.id) in ids_for(item.organisations)]
        org_node = {
            "id": f"organisation:{org.id}",
            "text": org.name,
            "kind": "organisation",
            "count": len(org_items),
            "filters": {"organisation_id": str(org.id)},
            "children": [],
        }

        function_ids = {}
        for item in org_items:
            for fn in item.functions:
                function_ids[fn.id] = fn
        for fn in sorted(function_ids.values(), key=lambda x: x.name.lower()):
            fn_items = [item for item in org_items if str(fn.id) in ids_for(item.functions)]
            fn_node = {
                "id": f"function:{fn.id}:org:{org.id}",
                "text": fn.name,
                "kind": "function",
                "count": len(fn_items),
                "filters": {"organisation_id": str(org.id), "function_id": str(fn.id)},
                "children": [],
            }

            topic_ids = {}
            for item in fn_items:
                for topic in item.topics:
                    topic_ids[topic.id] = topic
            for topic in sorted(topic_ids.values(), key=lambda x: x.name.lower()):
                topic_count = sum(1 for item in fn_items if str(topic.id) in ids_for(item.topics))
                fn_node["children"].append(
                    {
                        "id": f"topic:{topic.id}:function:{fn.id}:org:{org.id}",
                        "text": topic.name,
                        "kind": "topic",
                        "count": topic_count,
                        "filters": {
                            "organisation_id": str(org.id),
                            "function_id": str(fn.id),
                            "topic_id": str(topic.id),
                        },
                        "children": [],
                    }
                )
            org_node["children"].append(fn_node)
        root["children"].append(org_node)

    root["children"].extend(
        [
            {
                "id": "view:sprint",
                "text": "Nächster Sprint",
                "kind": "view",
                "count": len(sprint_membership_map(db, [item.id for item in items])),
                "filters": {"sprint": True},
                "children": [],
            },
            {
                "id": "view:review",
                "text": "Wiedervorlage",
                "kind": "view",
                "count": sum(1 for item in items if item.review_after is not None),
                "filters": {"has_review": True},
                "children": [],
            },
            {
                "id": "view:delegated",
                "text": "Delegiert",
                "kind": "view",
                "count": sum(1 for item in items if item.delegated_to),
                "filters": {"delegated": True},
                "children": [],
            },
        ]
    )
    return [root]


def seed_defaults(db: Session) -> None:
    defaults = {
        models.Organisation: ["FKM", "Giesserei Blöcher", "Familie", "Selbst"],
        models.WorkFunction: ["GF", "IT", "Personal", "Strategie", "Technik", "Privat"],
        models.Topic: ["KI", "Infrastruktur", "Informationssicherheit", "Personal", "Organisation", "Digitalisierung"],
    }
    for model, names in defaults.items():
        for name in names:
            slug = slugify(name)
            if db.scalar(select(model.id).where(model.slug == slug)) is None:
                db.add(model(name=name, slug=slug))
    db.commit()
