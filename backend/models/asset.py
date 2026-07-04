from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Asset(SQLModel, table=True):
    __tablename__: str = "assets"

    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str = Field(max_length=256)
    original_filename: str = Field(max_length=256)
    mime_type: str = Field(max_length=128)
    file_size: int = Field(default=0)
    url: str = Field(max_length=512)
    uploaded_by: Optional[int] = Field(default=None, foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.now)