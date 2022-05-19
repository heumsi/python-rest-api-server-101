from typing import Optional

from sqlmodel import Field, SQLModel

from src.models.utils import get_current_unix_timestamp

title_field = Field(description="게시글 제목", min_length=1, max_length=100,)
user_id_field = Field(description="게시글 작성자의 유저 ID", min_length=1, max_length=30)
content_field = Field(description="게시글 내용")
schema_extra = {
    "example": {
        "title": "첫 번째 게시글 입니다!",
        "content": "첫 번째 게시글 내용입니다!"
    }
}


class PostBase(SQLModel):
    title: str = Field(description="게시글 제목", min_length=1, max_length=100)
    content: str = content_field

    class Config:
        schema_extra = schema_extra


class Post(PostBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = user_id_field
    created_at: Optional[int] = Field(default_factory=get_current_unix_timestamp)
    updated_at: Optional[int] = Field(default_factory=get_current_unix_timestamp)


class PostPatch(PostBase):
    title: Optional[str] = title_field
    content: Optional[str] = content_field
