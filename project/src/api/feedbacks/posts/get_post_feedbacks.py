from typing import Optional, List

from fastapi import Query
from pydantic import BaseModel
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from src.database import engine
from src.models import post, user
from src.models.feedbacks import post_feedback


class GetPostFeedbacksResponse(BaseModel):
    class Data(BaseModel):
        id: int = post_feedback.id_field
        post_id: int = post.id_field
        user_id: str = user.id_field
        user_name: str = user.name_field
        like: bool
        created_at: int = post_feedback.created_at_field
        updated_at: int = post_feedback.updated_at_field

        class Config:
            title = 'GetPostFeedbacksResponse.Data'

    data: List[Data]


def handle(
    post_id: Optional[int] = None,
    offset: int = 0,
    limit: int = Query(default=100, lte=100)
) -> GetPostFeedbacksResponse:
    with Session(engine) as session:
        statement = (
            select(post_feedback.PostFeedback).offset(offset).limit(limit)
            .options(
                selectinload(post_feedback.PostFeedback.user),
            )
        )
        if post_id:
            statement = statement.where(post_feedback.PostFeedback.post_id == post_id)
        results = session.exec(statement)
        post_feedbacks_to_read = results.all()
        return GetPostFeedbacksResponse(
            data=[
                GetPostFeedbacksResponse.Data(
                    id=post_feedback_to_read.id,
                    post_id=post_feedback_to_read.post_id,
                    user_id=post_feedback_to_read.user_id,
                    user_name=post_feedback_to_read.user.name,
                    like=post_feedback_to_read.like,
                    created_at=post_feedback_to_read.created_at,
                    updated_at=post_feedback_to_read.updated_at
                )
                for post_feedback_to_read in post_feedbacks_to_read
            ]
        )
