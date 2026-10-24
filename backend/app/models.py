import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, String, Table, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, declarative_mixin, mapped_column, relationship

from .db import Base


def uuid_pk():
    return mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


item_organisations = Table(
    "item_organisations",
    Base.metadata,
    Column("item_id", UUID(as_uuid=True), ForeignKey("items.id", ondelete="CASCADE"), primary_key=True),
    Column("organisation_id", UUID(as_uuid=True), ForeignKey("organisations.id", ondelete="CASCADE"), primary_key=True),
)

item_functions = Table(
    "item_functions",
    Base.metadata,
    Column("item_id", UUID(as_uuid=True), ForeignKey("items.id", ondelete="CASCADE"), primary_key=True),
    Column("function_id", UUID(as_uuid=True), ForeignKey("work_functions.id", ondelete="CASCADE"), primary_key=True),
)

item_topics = Table(
    "item_topics",
    Base.metadata,
    Column("item_id", UUID(as_uuid=True), ForeignKey("items.id", ondelete="CASCADE"), primary_key=True),
    Column("topic_id", UUID(as_uuid=True), ForeignKey("topics.id", ondelete="CASCADE"), primary_key=True),
)

item_tags = Table(
    "item_tags",
    Base.metadata,
    Column("item_id", UUID(as_uuid=True), ForeignKey("items.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


@declarative_mixin
class NamedLookup:
    id: Mapped[uuid.UUID] = uuid_pk()
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(160))
    archived: Mapped[bool] = mapped_column(Boolean, default=False)


class Organisation(NamedLookup, Base):
    __tablename__ = "organisations"
    items: Mapped[list["Item"]] = relationship(secondary=item_organisations, back_populates="organisations")


class WorkFunction(NamedLookup, Base):
    __tablename__ = "work_functions"
    items: Mapped[list["Item"]] = relationship(secondary=item_functions, back_populates="functions")


class Topic(NamedLookup, Base):
    __tablename__ = "topics"
    items: Mapped[list["Item"]] = relationship(secondary=item_topics, back_populates="topics")


class Tag(NamedLookup, Base):
    __tablename__ = "tags"
    items: Mapped[list["Item"]] = relationship(secondary=item_tags, back_populates="tags")


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[uuid.UUID] = uuid_pk()
    type: Mapped[str] = mapped_column(String(50), index=True)
    name: Mapped[str] = mapped_column(String(160))
    writable: Mapped[bool] = mapped_column(Boolean, default=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    last_sync_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_success_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    objects: Mapped[list["SourceObject"]] = relationship(back_populates="source")


class SourceObject(Base):
    __tablename__ = "source_objects"
    __table_args__ = (UniqueConstraint("source_id", "external_id", name="uq_source_external_id"),)

    id: Mapped[uuid.UUID] = uuid_pk()
    source_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sources.id", ondelete="CASCADE"))
    external_id: Mapped[str] = mapped_column(String(300))
    external_type: Mapped[str | None] = mapped_column(String(80), nullable=True)
    external_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_state: Mapped[str] = mapped_column(String(30), default="active", index=True)
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_sync_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    source_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)

    source: Mapped[Source] = relationship(back_populates="objects")
    item: Mapped["Item | None"] = relationship(back_populates="source_object", uselist=False)


class Item(Base):
    __tablename__ = "items"

    id: Mapped[uuid.UUID] = uuid_pk()
    title: Mapped[str] = mapped_column(String(300), index=True)
    description: Mapped[str] = mapped_column(Text, default="")
    type: Mapped[str] = mapped_column(String(30), default="idea", index=True)
    state: Mapped[str] = mapped_column(String(30), default="open", index=True)
    due_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    review_after: Mapped[date | None] = mapped_column(Date, nullable=True)
    delegated_to: Mapped[str | None] = mapped_column(String(200), nullable=True)
    waiting_for: Mapped[str | None] = mapped_column(String(300), nullable=True)
    source_object_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("source_objects.id", ondelete="SET NULL"), nullable=True, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    organisations: Mapped[list[Organisation]] = relationship(
        secondary=item_organisations, back_populates="items", lazy="selectin"
    )
    functions: Mapped[list[WorkFunction]] = relationship(
        secondary=item_functions, back_populates="items", lazy="selectin"
    )
    topics: Mapped[list[Topic]] = relationship(secondary=item_topics, back_populates="items", lazy="selectin")
    tags: Mapped[list[Tag]] = relationship(secondary=item_tags, back_populates="items", lazy="selectin")
    source_object: Mapped[SourceObject | None] = relationship(back_populates="item", lazy="selectin")

    outgoing_relations: Mapped[list["ItemRelation"]] = relationship(
        foreign_keys="ItemRelation.from_item_id", back_populates="from_item", cascade="all, delete-orphan"
    )
    incoming_relations: Mapped[list["ItemRelation"]] = relationship(
        foreign_keys="ItemRelation.to_item_id", back_populates="to_item", cascade="all, delete-orphan"
    )


class ItemRelation(Base):
    __tablename__ = "item_relations"
    __table_args__ = (
        UniqueConstraint("from_item_id", "to_item_id", "type", name="uq_item_relation"),
    )

    id: Mapped[uuid.UUID] = uuid_pk()
    from_item_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("items.id", ondelete="CASCADE"))
    to_item_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("items.id", ondelete="CASCADE"))
    type: Mapped[str] = mapped_column(String(40), index=True)

    from_item: Mapped[Item] = relationship(foreign_keys=[from_item_id], back_populates="outgoing_relations")
    to_item: Mapped[Item] = relationship(foreign_keys=[to_item_id], back_populates="incoming_relations")


class Sprint(Base):
    __tablename__ = "sprints"
    __table_args__ = (UniqueConstraint("date", "state", name="uq_sprint_date_state"),)

    id: Mapped[uuid.UUID] = uuid_pk()
    date: Mapped[date] = mapped_column(Date, index=True)
    state: Mapped[str] = mapped_column(String(30), default="open", index=True)

    items: Mapped[list["SprintItem"]] = relationship(back_populates="sprint", cascade="all, delete-orphan")


class SprintItem(Base):
    __tablename__ = "sprint_items"
    __table_args__ = (UniqueConstraint("sprint_id", "item_id", name="uq_sprint_item"),)

    id: Mapped[uuid.UUID] = uuid_pk()
    sprint_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sprints.id", ondelete="CASCADE"))
    item_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("items.id", ondelete="CASCADE"))
    position: Mapped[int] = mapped_column(default=0)
    kind: Mapped[str] = mapped_column(String(20), default="focus")

    sprint: Mapped[Sprint] = relationship(back_populates="items")
    item: Mapped[Item] = relationship()
