from typing import List, Optional

from fastapi import Query, Request
from pydantic import BaseModel
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from src.api.comments.read_comment import ReadCommentResponse
from src.api.common import Link
from src.database import engine
from src.models import comment


class ReadCommentsResponse(BaseModel):
    data: List[ReadCommentResponse.Data]
    links: List[Link]


def handle(
    *,
    post_id: Optional[int] = None,
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    request: Request
) -> ReadCommentsResponse:
    with Session(engine) as session:
        statement = (
            select(comment.Comment).offset(offset).limit(limit)
            .options(
                selectinload(comment.Comment.user)
            )
        )
        if post_id:
            statement = statement.where(comment.Comment.post_id == post_id)
        results = session.exec(statement)
        comments_to_read = results.all()
        return ReadCommentsResponse(
            data=[
                ReadCommentResponse.Data(
                    id=comment_to_read.id,
                    content=comment_to_read.content,
                    created_at=comment_to_read.created_at,
                    updated_at=comment_to_read.updated_at,
                    post=ReadCommentResponse.Data.Post(
                        id=comment_to_read.post_id,
                    ),
                    user=ReadCommentResponse.Data.User(
                        id=comment_to_read.user.id,
                        name=comment_to_read.user.name,
                    ),
                    links=[
                        Link(
                            rel="self",
                            href=f"{request.base_url}comments/{comment_to_read.id}"
                        ),
                        Link(
                            rel="post",
                            href=f"{request.base_url}posts/{comment_to_read.post_id}"
                        )
                    ]
                )
                for comment_to_read in comments_to_read
            ],
            links=[
                Link(
                    rel="self",
                    href=request.url._url
                )
            ]
        )
