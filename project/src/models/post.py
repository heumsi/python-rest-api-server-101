from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.models.comment import Comment
    from src.models.feedbacks.post_feedback import PostFeedback

from src.models.user import User
from src.models.utils import get_current_unix_timestamp

id_field = Field(default=None, primary_key=True)
title_field = Field(description="게시글 제목", min_length=1, max_length=100)
content_field = Field(description="게시글 내용")
created_at_field = Field(default_factory=get_current_unix_timestamp)
updated_at_field = Field(default_factory=get_current_unix_timestamp)


class Post(SQLModel, table=True):
    id: Optional[int] = id_field
    title: str = title_field
    user_id: str = Field(foreign_key="user.id")
    content: str = content_field
    created_at: Optional[int] = created_at_field
    updated_at: Optional[int] = updated_at_field

    user: User = Relationship()
    comments: List["Comment"] = Relationship()
    feedbacks: List["PostFeedback"] = Relationship()
