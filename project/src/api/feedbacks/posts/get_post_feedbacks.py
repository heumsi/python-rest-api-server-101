from typing import List, Optional

from fastapi import Query, Request
from sqlalchemy.orm import selectinload
from sqlmodel import Session, func, select

from src.api.common import Link, Pagination, SchemaModel, get_links_for_pagination
from src.database import engine
from src.models import post, user
from src.models.feedbacks import post_feedback


class GetPostFeedbacksResponse(SchemaModel):
    class Data(SchemaModel):
        id: int = post_feedback.id_field
        like: bool
        created_at: int = post_feedback.created_at_field
        updated_at: int = post_feedback.updated_at_field
        links: List[Link]

        class Post(SchemaModel):
            id: int = post.id_field

            class Config:
                title = "GetPostFeedbacksResponse.Data"

        class User(SchemaModel):
            id: str = user.id_field
            name: str = user.name_field

            class Config:
                title = "GetPostFeedbacksResponse.Data"

        post: Post
        user: User

        class Config:
            title = "GetPostFeedbacksResponse.Data"

    pagination: Pagination
    data: List[Data]
    links: List[Link]


def _get_total(session: Session, post_id: Optional[int] = None) -> int:
    """ get total count of rows for pagination """
    statement = select([func.count(post_feedback.PostFeedback.id)])
    if post_id:
        statement = statement.where(post_feedback.PostFeedback.post_id == post_id)
    return session.exec(statement).one()  # type: ignore


def _get_post_feedbacks(session: Session, offset: int, limit: int, post_id: Optional[int] = None) -> List[post_feedback.PostFeedback]:
    """ get all rows """
    statement = (
        select(post_feedback.PostFeedback)
        .order_by(post_feedback.PostFeedback.id)
        .offset(offset)
        .limit(limit)
        .options(
            selectinload(post_feedback.PostFeedback.user),
        )
    )
    if post_id:
        statement = statement.where(post_feedback.PostFeedback.post_id == post_id)
    results = session.exec(statement)
    return results.all()


def handle(
    *,
    post_id: Optional[int] = None,
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    request: Request,
) -> GetPostFeedbacksResponse:
    with Session(engine) as session:
        total = _get_total(session, post_id)
        post_feedbacks_to_read= _get_post_feedbacks(session, offset, limit, post_id)
        return GetPostFeedbacksResponse(
            pagination=Pagination(offset=offset, limit=limit, total=total),
            data=[
                GetPostFeedbacksResponse.Data(
                    id=post_feedback_to_read.id,
                    like=post_feedback_to_read.like,
                    created_at=post_feedback_to_read.created_at,
                    updated_at=post_feedback_to_read.updated_at,
                    post=GetPostFeedbacksResponse.Data.Post(
                        id=post_feedback_to_read.post_id
                    ),
                    user=GetPostFeedbacksResponse.Data.User(
                        id=post_feedback_to_read.user_id,
                        name=post_feedback_to_read.user.name,
                    ),
                    links=[
                        Link(
                            rel="post",
                            href=f"{request.base_url}posts/{post_feedback_to_read.post_id}",
                        )
                    ],
                )
                for post_feedback_to_read in post_feedbacks_to_read
            ],
            links=get_links_for_pagination(offset, limit, total, request),
        )
