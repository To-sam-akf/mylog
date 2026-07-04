from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class PageVersion(SQLModel, table=True):
    __tablename__:str= "page_versions"

    id: Optional[int] = Field(default=None, primary_key=True)
    page_id: int = Field(foreign_key="pages.id",index=True)
    title: str = Field(max_length=256)
    content: str = Field(max_length=2048)
    content_json: Optional[str] = Field(default=None)
    content_markdown: Optional[str] = Field(default=None, max_length=2048)
    created_by: Optional[int] = Field(default=None, foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.now)