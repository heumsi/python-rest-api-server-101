from sqlmodel import SQLModel, Field, Relationship

from src.models.post import Post
from src.models.user import User
from src.models.utils import get_current_unix_timestamp

id_field = Field(default=None, primary_key=True)
content_field = Field(description="댓글 내용", min_length=1, max_length=300)
created_at_field = Field(default_factory=get_current_unix_timestamp)
updated_at_field = Field(default_factory=get_current_unix_timestamp)


class Comment(SQLModel, table=True):
    id: int = id_field
    post_id: int = Field(foreign_key="post.id")
    user_id: str = Field(foreign_key="user.id")
    content: str = content_field
    created_at: int = created_at_field
    updated_at: int = updated_at_field

    post: Post = Relationship()
    user: User = Relationship()
