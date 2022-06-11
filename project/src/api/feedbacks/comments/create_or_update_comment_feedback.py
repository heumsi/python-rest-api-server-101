from typing import Union, Literal

from fastapi import Depends, HTTPException, status, Response
from pydantic import BaseModel
from sqlmodel import Session, select

from src.api.auth.utils import GetAuthorizedUser
from src.database import engine
from src.models import comment, user
from src.models.feedbacks import comment_feedback
from src.models.utils import get_current_unix_timestamp


class BaseResponse(BaseModel):
    class Data(BaseModel):
        id: int = comment_feedback.id_field
        comment_id: int = comment.id_field
        user_id: str = user.id_field
        like: bool
        created_at: int = comment_feedback.created_at_field
        updated_at: int = comment_feedback.updated_at_field

        class Config:
            title = 'CreateOrUpdateCommentFeedbackBaseResponse.Data'

    data: Data


class CreateCommentFeedbackResponse(BaseResponse):
    class Data(BaseResponse.Data):
        class Config:
            title = 'CreateCommentFeedbackResponse.Data'


class UpdateCommentFeedbackResponse(BaseResponse):
    class Data(BaseResponse.Data):
        class Config:
            title = 'UpdateCommentFeedbackResponse.Data'


def handle(
    comment_id: int,
    like_or_dislike: Literal["like", "dislike"],
    response: Response,
    current_user: user.User = Depends(GetAuthorizedUser(allowed_roles=[user.Role.ADMIN, user.Role.COMMON])),
) -> Union[CreateCommentFeedbackResponse, UpdateCommentFeedbackResponse]:
    with Session(engine) as session:
        existing_comment = session.get(comment.Comment, comment_id)
        if not existing_comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

        statement = select(comment_feedback.CommentFeedback).where(
            comment_feedback.CommentFeedback.comment_id == existing_comment.id,
            comment_feedback.CommentFeedback.user_id == current_user.id,
        )
        results = session.exec(statement)
        existing_comment_feedback = results.first()

        if existing_comment_feedback:
            if like_or_dislike == "like":
                existing_comment_feedback.like = True
            else:
                existing_comment_feedback.like = False
            existing_comment_feedback.updated_at = get_current_unix_timestamp()
            session.add(existing_comment_feedback)
            session.commit()
            session.refresh(existing_comment_feedback)

            response.status_code = status.HTTP_200_OK
            return UpdateCommentFeedbackResponse(
                data=UpdateCommentFeedbackResponse.Data(
                    id=existing_comment_feedback.id,
                    comment_id=existing_comment_feedback.comment_id,
                    user_id=existing_comment_feedback.user_id,
                    like=existing_comment_feedback.like,
                    created_at=existing_comment_feedback.created_at,
                    updated_at=existing_comment_feedback.updated_at
                )
            )
        else:
            if like_or_dislike == "like":
                like = True
            else:
                like = False
            new_comment_feedback = comment_feedback.CommentFeedback(
                comment_id=existing_comment.id,
                user_id=current_user.id,
                like=like,
                comment=existing_comment,
                user=current_user
            )
            session.add(new_comment_feedback)
            session.commit()
            session.refresh(new_comment_feedback)

            response.status_code = status.HTTP_201_CREATED
            return CreateCommentFeedbackResponse(
                data=CreateCommentFeedbackResponse.Data(
                    id=new_comment_feedback.id,
                    comment_id=new_comment_feedback.comment_id,
                    user_id=new_comment_feedback.user_id,
                    like=new_comment_feedback.like,
                    created_at=new_comment_feedback.created_at,
                    updated_at=new_comment_feedback.updated_at
                )
            )
