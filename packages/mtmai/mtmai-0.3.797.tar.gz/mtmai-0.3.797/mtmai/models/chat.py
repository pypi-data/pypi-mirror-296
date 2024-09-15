import uuid
from datetime import datetime

from sqlmodel import JSON, Column, Field, SQLModel


class ChatThread(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    # id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
    name: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

    user_id: str = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    user_name: str = Field(max_length=255)
    tags: list[str] = Field(default=[], sa_column=Column(JSON))
    meta: dict | None = Field(default={}, sa_column=Column(JSON))


class ChatStep(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    type: str = Field(max_length=255)
    thread_id: uuid.UUID = Field(...)
    parent_id: uuid.UUID | None = Field(default=None)
    disable_feedback: bool = Field(...)
    streaming: bool = Field(...)
    wait_for_answer: bool | None = Field(default=None)
    is_error: bool | None = Field(default=None)
    meta: dict | None = Field(default=None, sa_column=Column(JSON))
    tags: list[str] = Field(default=[], sa_column=Column(JSON))
    input: str | None = Field(default=None)
    output: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    start: datetime | None = Field(default=None)
    end: datetime | None = Field(default=None)
    generation: dict | None = Field(default=None, sa_column=Column(JSON))
    show_input: str | None = Field(default=None)
    language: str | None = Field(default=None)
    indent: int | None = Field(default=None)


class ChatElement(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    thread_id: uuid.UUID | None = Field(default=None)
    type: str | None = Field(default=None)
    url: str | None = Field(default=None)
    chainlit_key: str | None = Field(default=None)
    name: str = Field(...)
    display: str | None = Field(default=None)
    object_key: str | None = Field(default=None)
    size: str | None = Field(default=None)
    page: int | None = Field(default=None)
    language: str | None = Field(default=None)
    for_id: uuid.UUID | None = Field(default=None)
    mime: str | None = Field(default=None)


class ChatFeedback(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    for_id: uuid.UUID = Field(...)
    thread_id: uuid.UUID = Field(...)
    value: int = Field(...)
    comment: str | None = Field(default=None)
