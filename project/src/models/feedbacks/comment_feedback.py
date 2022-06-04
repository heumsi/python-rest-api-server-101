from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from src.models.comment import Comment
from src.models.user import User
from src.models.utils import get_current_unix_timestamp

id_field = Field(default=None, primary_key=True)
created_at_field = Field(default_factory=get_current_unix_timestamp)
updated_at_field = Field(default_factory=get_current_unix_timestamp)


class CommentFeedback(SQLModel, table=True):
    __tablename__ = "feedback_comment"

    id: Optional[int] = id_field
    comment_id: int = Field(foreign_key="comment.id")
    user_id: str = Field(foreign_key="user.id")
    like: bool
    created_at: int = created_at_field
    updated_at: int = updated_at_field

    comment: Comment = Relationship()
    user: User = Relationship()
