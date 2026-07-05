from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Field, SQLModel, func


class Work(SQLModel, table=True):
    __tablename__: str = "works"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=128)
    tech: str = Field(max_length=256)
    desc: str
    status: str = Field(max_length=64)
    github: str = Field(max_length=512)
    color: str = Field(default="yellow", max_length=32)
    sort_order: int = Field(default=0, index=True)
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime, server_default=func.now()),
    )
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})


class WorkPageSetting(SQLModel, table=True):
    __tablename__: str = "work_page_settings"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(default="WORKS!", max_length=128)
    subtitle: str = Field(default="CREATE · BUILD · SHOW", max_length=256)
    description: str
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})
