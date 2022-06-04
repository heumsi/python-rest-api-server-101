from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from src.models.post import Post
from src.models.user import User
from src.models.utils import get_current_unix_timestamp

id_field = Field(default=None, primary_key=True)
created_at_field = Field(default_factory=get_current_unix_timestamp)
updated_at_field = Field(default_factory=get_current_unix_timestamp)


class PostFeedback(SQLModel, table=True):
    __tablename__ = "feedback_post"

    id: Optional[int] = id_field
    post_id: int = Field(foreign_key="post.id")
    user_id: str = Field(foreign_key="user.id")
    like: bool
    created_at: int = created_at_field
    updated_at: int = updated_at_field

    post: Post = Relationship(back_populates="feedbacks")
    user: User = Relationship()
