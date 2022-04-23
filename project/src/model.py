import time
from typing import Optional

from sqlmodel import SQLModel, Field


class PostBase(SQLModel):
    title: str
    author: str
    content: str


class Post(PostBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[int] = Field(default_factory=time.time)
    updated_at: Optional[int] = Field(default_factory=time.time)


class PostUpdate(SQLModel):
    title: Optional[str] = None
    author: Optional[str] = None
    content: Optional[str] = None
