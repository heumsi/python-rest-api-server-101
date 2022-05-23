from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session

from src.database import engine
from src.models import comment, user, post
from src.models.comment import Comment


class ReadCommentResponse(BaseModel):
    id: int = comment.id_field
    post_id: int = post.id_field
    content: str = comment.content_field
    user_id: str = user.id_field
    user_name: str = user.name_field
    created_at: int = comment.created_at_field
    updated_at: int = comment.updated_at_field


def handle(comment_id: int) -> ReadCommentResponse:
    with Session(engine) as session:
        comment_to_read = session.get(Comment, comment_id)
        if not comment_to_read:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        return ReadCommentResponse(
            id=comment_to_read.id,
            post_id=comment_to_read.post_id,
            content=comment_to_read.content,
            user_id=comment_to_read.user.id,
            user_name=comment_to_read.user.name,
            created_at=comment_to_read.created_at,
            updated_at=comment_to_read.updated_at,
        )
