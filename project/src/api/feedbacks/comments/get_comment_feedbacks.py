from typing import List, Optional

from fastapi import Query, Request
from sqlalchemy.orm import selectinload
from sqlmodel import Session, func, select

from src.api.common import Link, Pagination, SchemaModel, get_links_for_pagination
from src.database import engine
from src.models import comment, user
from src.models.feedbacks import comment_feedback


class GetCommentFeedbacksResponse(SchemaModel):
    class Data(SchemaModel):
        id: int = comment_feedback.id_field
        like: bool
        created_at: int = comment_feedback.created_at_field
        updated_at: int = comment_feedback.updated_at_field
        links: List[Link]

        class Comment(SchemaModel):
            id: int = comment.id_field

            class Config:
                title = "GetCommentFeedbacksResponse.Data.Comment"

        class User(SchemaModel):
            id: str = user.id_field
            name: str = user.name_field

            class Config:
                title = "GetCommentFeedbacksResponse.Data.User"

        comment: Comment
        user: User

        class Config:
            title = "GetCommentFeedbacksResponse.Data"

    pagination: Pagination
    data: List[Data]
    links: List[Link]


def handle(
    *,
    comment_id: Optional[int] = None,
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    request: Request,
) -> GetCommentFeedbacksResponse:
    with Session(engine) as session:
        # get total count of rows for pagination
        statement = select([func.count(comment_feedback.CommentFeedback.id)])
        total = session.exec(statement).one()

        # get all rows
        statement = (
            select(comment_feedback.CommentFeedback)
            .offset(offset)
            .limit(limit)
            .options(
                selectinload(comment_feedback.CommentFeedback.user),
            )
        )
        if comment_id:
            statement = statement.where(
                comment_feedback.CommentFeedback.comment_id == comment_id
            )
        results = session.exec(statement)
        comment_feedbacks_to_read = results.all()
        return GetCommentFeedbacksResponse(
            pagination=Pagination(offset=offset, limit=limit, total=total),
            data=[
                GetCommentFeedbacksResponse.Data(
                    id=comment_feedback_to_read.id,
                    like=comment_feedback_to_read.like,
                    created_at=comment_feedback_to_read.created_at,
                    updated_at=comment_feedback_to_read.updated_at,
                    comment=GetCommentFeedbacksResponse.Data.Comment(
                        id=comment_feedback_to_read.comment_id,
                    ),
                    user=GetCommentFeedbacksResponse.Data.User(
                        id=comment_feedback_to_read.user_id,
                        name=comment_feedback_to_read.user.name,
                    ),
                    links=[
                        Link(
                            rel="comment",
                            href=f"{request.base_url}comments/{comment_feedback_to_read.comment_id}",
                        )
                    ],
                )
                for comment_feedback_to_read in comment_feedbacks_to_read
            ],
            links=get_links_for_pagination(offset, limit, total, request),
        )
