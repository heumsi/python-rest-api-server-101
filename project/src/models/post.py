from typing import Optional

from sqlmodel import Field, SQLModel

from src.models.utils import get_current_unix_timestamp

id_field = Field(default=None, primary_key=True)
title_field = Field(description="게시글 제목", min_length=1, max_length=100)
user_id_field = Field(description="게시글 작성자의 유저 ID", min_length=1, max_length=30)
content_field = Field(description="게시글 내용")
created_at_field = Field(default_factory=get_current_unix_timestamp)
updated_at_field = Field(default_factory=get_current_unix_timestamp)


class Post(SQLModel, table=True):
    id: Optional[int] = id_field
    title: str = title_field
    user_id: str = user_id_field
    content: str = content_field
    created_at: Optional[int] = created_at_field
    updated_at: Optional[int] = updated_at_field
