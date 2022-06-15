from typing import Union, Literal

from fastapi import Depends, HTTPException, status, Response
from sqlmodel import Session, select

from src.api.auth.utils import GetAuthorizedUser
from src.api.common import SchemaModel
from src.database import engine
from src.models import post, user
from src.models.feedbacks import post_feedback
from src.models.utils import get_current_unix_timestamp


class BaseResponse(SchemaModel):
    class Data(SchemaModel):
        id: int = post_feedback.id_field
        like: bool
        created_at: int = post_feedback.created_at_field
        updated_at: int = post_feedback.updated_at_field

        class Post(SchemaModel):
            id: int = post.id_field

            class Config:
                title = "CreateOrUpdatePostFeedbackBaseResponse.Data"

        class User(SchemaModel):
            id: str = user.id_field

            class Config:
                title = "CreateOrUpdatePostFeedbackBaseResponse.Data"

        post: Post
        user: User

        class Config:
            title = "CreateOrUpdatePostFeedbackBaseResponse.Data"

    data: Data


class CreatePostFeedbackResponse(BaseResponse):
    class Data(BaseResponse.Data):
        class Config:
            title = "CreatePostFeedbackResponse.Data"


class UpdatePostFeedbackResponse(BaseResponse):
    class Data(BaseResponse.Data):
        class Config:
            title = "UpdatePostFeedbackResponse.Data"


def handle(
    post_id: int,
    like_or_dislike: Literal["like", "dislike"],
    response: Response,
    current_user: user.User = Depends(
        GetAuthorizedUser(allowed_roles=[user.Role.ADMIN, user.Role.COMMON])
    ),
) -> Union[CreatePostFeedbackResponse, UpdatePostFeedbackResponse]:
    with Session(engine) as session:
        existing_post = session.get(post.Post, post_id)
        if not existing_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )

        statement = select(post_feedback.PostFeedback).where(
            post_feedback.PostFeedback.post_id == existing_post.id,
            post_feedback.PostFeedback.user_id == current_user.id,
        )
        results = session.exec(statement)
        existing_post_feedback = results.first()

        if existing_post_feedback:
            if like_or_dislike == "like":
                existing_post_feedback.like = True
            else:
                existing_post_feedback.like = False
            existing_post_feedback.updated_at = get_current_unix_timestamp()
            session.add(existing_post_feedback)
            session.commit()
            session.refresh(existing_post_feedback)

            response.status_code = status.HTTP_200_OK
            return UpdatePostFeedbackResponse(
                data=UpdatePostFeedbackResponse.Data(
                    id=existing_post_feedback.id,
                    like=existing_post_feedback.like,
                    created_at=existing_post_feedback.created_at,
                    updated_at=existing_post_feedback.updated_at,
                    post=UpdatePostFeedbackResponse.Data.Post(
                        id=existing_post_feedback.post_id
                    ),
                    user=UpdatePostFeedbackResponse.Data.User(
                        id=existing_post_feedback.user_id,
                    ),
                )
            )
        else:
            if like_or_dislike == "like":
                like = True
            else:
                like = False
            new_post_feedback = post_feedback.PostFeedback(
                post_id=existing_post.id,
                user_id=current_user.id,
                like=like,
                post=existing_post,
                user=current_user,
            )
            session.add(new_post_feedback)
            session.commit()
            session.refresh(new_post_feedback)

            response.status_code = status.HTTP_201_CREATED
            return CreatePostFeedbackResponse(
                data=CreatePostFeedbackResponse.Data(
                    id=new_post_feedback.id,
                    like=new_post_feedback.like,
                    created_at=new_post_feedback.created_at,
                    updated_at=new_post_feedback.updated_at,
                    post=UpdatePostFeedbackResponse.Data.Post(
                        id=new_post_feedback.post_id
                    ),
                    user=UpdatePostFeedbackResponse.Data.User(
                        id=new_post_feedback.user_id,
                    ),
                )
            )
