import time
from typing import Optional

from sqlmodel import SQLModel, Field


def get_current_unix_timestamp() -> int:
    return int(time.time())


title_field = Field(description="게시글 제목", min_length=1, max_length=100,)
author_field = Field(description="게시글 작성자", min_length=1, max_length=30)
content_field = Field(description="게시글 내용")
schema_extra = {
    "example": {
        "title": "첫 번째 게시글 입니다!",
        "author": "heumsi",
        "content": "첫 번째 게시글 내용입니다!"
    }
}


class PostBase(SQLModel):
    title: str = Field(description="게시글 제목", min_length=1, max_length=100)
    author: str = author_field
    content: str = content_field

    class Config:
        schema_extra = schema_extra


class Post(PostBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[int] = Field(default_factory=get_current_unix_timestamp)
    updated_at: Optional[int] = Field(default_factory=get_current_unix_timestamp)


class PostPatch(PostBase):
    title: Optional[str] = title_field
    author: Optional[str] = author_field
    content: Optional[str] = content_field
