from typing import List, Optional

from fastapi import Query, Request
from sqlalchemy.orm import selectinload
from sqlmodel import Session, func, select

from src.api.common import Link, Pagination, SchemaModel, get_links_for_pagination
from src.api.v1.comments.read_comment import ReadCommentResponse
from src.database import engine
from src.models import comment


class ReadCommentsResponse(SchemaModel):
    pagination: Pagination
    data: List[ReadCommentResponse.Data]
    links: List[Link]


def _get_total(session: Session, post_id: Optional[int] = None) -> int:
    """get total count of rows for pagination"""
    statement = select([func.count(comment.Comment.id)])
    if post_id:
        statement = statement.where(comment.Comment.post_id == post_id)
    return session.exec(statement).one()  # type: ignore


def _get_comments(
    session: Session, offset: int, limit: int, post_id: Optional[int] = None
) -> List[comment.Comment]:
    """get all rows"""
    statement = (
        select(comment.Comment)
        .order_by(comment.Comment.id)
        .offset(offset)
        .limit(limit)
        .options(selectinload(comment.Comment.user))
    )
    if post_id:
        statement = statement.where(comment.Comment.post_id == post_id)
    results = session.exec(statement)
    return results.all()


def handle(
    *,
    post_id: Optional[int] = None,
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    request: Request,
) -> ReadCommentsResponse:
    with Session(engine) as session:
        total = _get_total(session, post_id)
        comments_to_read = _get_comments(session, offset, limit, post_id)
        return ReadCommentsResponse(
            pagination=Pagination(offset=offset, limit=limit, total=total),
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
                            href=f"{request.base_url}v1/comments/{comment_to_read.id}",
                        ),
                        Link(
                            rel="post",
                            href=f"{request.base_url}v1/posts/{comment_to_read.post_id}",
                        ),
                    ],
                )
                for comment_to_read in comments_to_read
            ],
            links=get_links_for_pagination(offset, limit, total, request),
        )
