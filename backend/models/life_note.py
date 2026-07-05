from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Field, SQLModel, func


class LifeNote(SQLModel, table=True):
    __tablename__: str = "life_notes"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=128)
    content: str
    content_markdown: Optional[str] = Field(default=None)
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime, server_default=func.now()),
    )
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})
