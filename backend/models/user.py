from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column, DateTime,func

class User(SQLModel,table=True):
    __tablename__:str="users"
    id: Optional[int] = Field(default=None,primary_key=True)
    username:str=Field(index=True, unique=True, max_length=64)
    password_hash:str = Field(max_length=256)
    role:str=Field(default="admin",max_length=32)
    created_at:datetime=Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime,server_default=func.now())
                              )
    update_at:datetime=Field(default_factory=datetime.now)

