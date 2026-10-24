"""initial IMP schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-10-25
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    uuid = postgresql.UUID(as_uuid=True)

    for table in ["organisations", "work_functions", "topics", "tags"]:
        op.create_table(
            table,
            sa.Column("id", uuid, primary_key=True),
            sa.Column("slug", sa.String(length=120), nullable=False),
            sa.Column("name", sa.String(length=160), nullable=False),
            sa.Column("archived", sa.Boolean(), nullable=False, server_default=sa.false()),
            sa.UniqueConstraint("slug"),
        )
        op.create_index(f"ix_{table}_slug", table, ["slug"], unique=True)

    op.create_table(
        "sources",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("type", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("writable", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("last_sync_at", sa.DateTime(timezone=True)),
        sa.Column("last_success_at", sa.DateTime(timezone=True)),
    )
    op.create_index("ix_sources_type", "sources", ["type"])

    op.create_table(
        "source_objects",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("source_id", uuid, sa.ForeignKey("sources.id", ondelete="CASCADE"), nullable=False),
        sa.Column("external_id", sa.String(length=300), nullable=False),
        sa.Column("external_type", sa.String(length=80)),
        sa.Column("external_url", sa.Text()),
        sa.Column("source_state", sa.String(length=30), nullable=False, server_default="active"),
        sa.Column("last_seen_at", sa.DateTime(timezone=True)),
        sa.Column("last_sync_at", sa.DateTime(timezone=True)),
        sa.Column("source_hash", sa.String(length=128)),
        sa.UniqueConstraint("source_id", "external_id", name="uq_source_external_id"),
    )
    op.create_index("ix_source_objects_source_state", "source_objects", ["source_state"])

    op.create_table(
        "items",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("title", sa.String(length=300), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("type", sa.String(length=30), nullable=False, server_default="idea"),
        sa.Column("state", sa.String(length=30), nullable=False, server_default="open"),
        sa.Column("due_at", sa.Date()),
        sa.Column("review_after", sa.Date()),
        sa.Column("delegated_to", sa.String(length=200)),
        sa.Column("waiting_for", sa.String(length=300)),
        sa.Column("source_object_id", uuid, sa.ForeignKey("source_objects.id", ondelete="SET NULL"), unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_items_title", "items", ["title"])
    op.create_index("ix_items_type", "items", ["type"])
    op.create_index("ix_items_state", "items", ["state"])

    associations = [
        ("item_organisations", "organisation_id", "organisations"),
        ("item_functions", "function_id", "work_functions"),
        ("item_topics", "topic_id", "topics"),
        ("item_tags", "tag_id", "tags"),
    ]
    for table, foreign_column, foreign_table in associations:
        op.create_table(
            table,
            sa.Column("item_id", uuid, sa.ForeignKey("items.id", ondelete="CASCADE"), primary_key=True),
            sa.Column(foreign_column, uuid, sa.ForeignKey(f"{foreign_table}.id", ondelete="CASCADE"), primary_key=True),
        )

    op.create_table(
        "item_relations",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("from_item_id", uuid, sa.ForeignKey("items.id", ondelete="CASCADE"), nullable=False),
        sa.Column("to_item_id", uuid, sa.ForeignKey("items.id", ondelete="CASCADE"), nullable=False),
        sa.Column("type", sa.String(length=40), nullable=False),
        sa.UniqueConstraint("from_item_id", "to_item_id", "type", name="uq_item_relation"),
    )
    op.create_index("ix_item_relations_type", "item_relations", ["type"])

    op.create_table(
        "sprints",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("state", sa.String(length=30), nullable=False, server_default="open"),
        sa.UniqueConstraint("date", "state", name="uq_sprint_date_state"),
    )
    op.create_index("ix_sprints_date", "sprints", ["date"])
    op.create_index("ix_sprints_state", "sprints", ["state"])

    op.create_table(
        "sprint_items",
        sa.Column("id", uuid, primary_key=True),
        sa.Column("sprint_id", uuid, sa.ForeignKey("sprints.id", ondelete="CASCADE"), nullable=False),
        sa.Column("item_id", uuid, sa.ForeignKey("items.id", ondelete="CASCADE"), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("kind", sa.String(length=20), nullable=False, server_default="focus"),
        sa.UniqueConstraint("sprint_id", "item_id", name="uq_sprint_item"),
    )


def downgrade() -> None:
    for table in [
        "sprint_items",
        "sprints",
        "item_relations",
        "item_tags",
        "item_topics",
        "item_functions",
        "item_organisations",
        "items",
        "source_objects",
        "sources",
        "tags",
        "topics",
        "work_functions",
        "organisations",
    ]:
        op.drop_table(table)
