from typing import Optional, List

from fastapi import Query
from pydantic import BaseModel
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from src.database import engine
from src.models import comment, user
from src.models.feedbacks import comment_feedback


class GetCommentFeedbackResponse(BaseModel):
    id: int = comment_feedback.id_field
    comment_id: int = comment.id_field
    user_id: str = user.id_field
    user_name: str = user.name_field
    like: bool
    created_at: int = comment_feedback.created_at_field
    updated_at: int = comment_feedback.updated_at_field


class GetCommentFeedbacksResponse(BaseModel):
    items: List[GetCommentFeedbackResponse]


def handle(
    comment_id: Optional[int] = None,
    offset: int = 0,
    limit: int = Query(default=100, lte=100)
) -> GetCommentFeedbacksResponse:
    with Session(engine) as session:
        statement = (
            select(comment_feedback.CommentFeedback).offset(offset).limit(limit)
            .options(
                selectinload(comment_feedback.CommentFeedback.user),
            )
        )
        if comment_id:
            statement = statement.where(comment_feedback.CommentFeedback.comment_id == comment_id)
        results = session.exec(statement)
        comment_feedbacks_to_read = results.all()
        return GetCommentFeedbacksResponse(
            items=[
                GetCommentFeedbackResponse(
                    id=comment_feedback_to_read.id,
                    comment_id=comment_feedback_to_read.comment_id,
                    user_id=comment_feedback_to_read.user_id,
                    user_name=comment_feedback_to_read.user.name,
                    like=comment_feedback_to_read.like,
                    created_at=comment_feedback_to_read.created_at,
                    updated_at=comment_feedback_to_read.updated_at
                )
                for comment_feedback_to_read in comment_feedbacks_to_read
            ]
        )
