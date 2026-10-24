import uuid
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


ItemType = Literal["idea", "action", "commitment", "process", "waiting", "reference"]
ItemState = Literal["open", "active", "done", "cancelled", "archived"]


class LookupOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    slug: str
    name: str


class LookupCreate(BaseModel):
    name: str = Field(min_length=1, max_length=160)


class LookupUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=160)


class ItemBase(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    description: str = ""
    type: ItemType = "idea"
    state: ItemState = "open"
    due_at: date | None = None
    review_after: date | None = None
    delegated_to: str | None = None
    waiting_for: str | None = None


class ItemCreate(ItemBase):
    organisation_ids: list[uuid.UUID] = Field(default_factory=list)
    function_ids: list[uuid.UUID] = Field(default_factory=list)
    topic_ids: list[uuid.UUID] = Field(default_factory=list)
    tag_ids: list[uuid.UUID] = Field(default_factory=list)


class ItemUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=300)
    description: str | None = None
    type: ItemType | None = None
    state: ItemState | None = None
    due_at: date | None = None
    review_after: date | None = None
    delegated_to: str | None = None
    waiting_for: str | None = None
    organisation_ids: list[uuid.UUID] | None = None
    function_ids: list[uuid.UUID] | None = None
    topic_ids: list[uuid.UUID] | None = None
    tag_ids: list[uuid.UUID] | None = None


class SourceInfo(BaseModel):
    source_type: str
    source_name: str
    external_id: str
    external_url: str | None = None
    source_state: str


class ItemOut(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    organisations: list[LookupOut]
    functions: list[LookupOut]
    topics: list[LookupOut]
    tags: list[LookupOut]
    source: SourceInfo | None = None
    in_current_sprint: bool = False
    sprint_kind: str | None = None
    created_at: datetime
    updated_at: datetime


class SprintToggle(BaseModel):
    included: bool
    kind: Literal["focus", "optional"] = "focus"


class TreeNode(BaseModel):
    id: str
    text: str
    kind: str
    count: int
    filters: dict[str, str | bool] = Field(default_factory=dict)
    children: list["TreeNode"] = Field(default_factory=list)


class LookupsOut(BaseModel):
    organisations: list[LookupOut]
    functions: list[LookupOut]
    topics: list[LookupOut]
    tags: list[LookupOut]
