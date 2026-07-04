from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, func, DateTime, Column

class Page(SQLModel, table=True):
    __tablename__ : str =  "pages"

    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = Field(index=True, unique=True, max_length=128)
    title: str = Field(index=True, max_length=128)
    content: str
    content_markdown: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now,sa_column=Column(DateTime,server_default=func.now()))
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})