from typing import List, Optional

from fastapi import Query
from pydantic import BaseModel
from sqlmodel import Session, select

from src.api.comments.read_comment import ReadCommentResponse
from src.database import engine
from src.models import comment, post


class ReadCommentsResponse(BaseModel):
    items: List[ReadCommentResponse]


def handle(
    post_id: Optional[int] = None,
    offset: int = 0,
    limit: int = Query(default=100, lte=100)
) -> ReadCommentsResponse:
    with Session(engine) as session:
        statement = select(comment.Comment).offset(offset).limit(limit)
        if post_id:
            statement = statement.where(comment.Comment.post_id == post_id)
        results = session.exec(statement)
        comments_to_read = results.all()
        return ReadCommentsResponse(
            items=[
                ReadCommentResponse(
                    id=comment_to_read.id,
                    post_id=comment_to_read.post_id,
                    content=comment_to_read.content,
                    user_id=comment_to_read.user_id,
                    user_name=comment_to_read.user.name,
                    created_at=comment_to_read.created_at,
                    updated_at=comment_to_read.updated_at,
                )
                for comment_to_read in comments_to_read
            ]
        )