from fastapi import Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session
from starlette import status

from src.api.auth.utils import GetAuthorizedUser
from src.database import engine
from src.models import post, user
from src.models.utils import get_current_unix_timestamp


class UpdatePostRequest(BaseModel):
    title: str = post.title_field
    content: str = post.content_field


class UpdatePostResponse(BaseModel):
    class Data(BaseModel):
        id: int = post.id_field
        title: str = post.title_field
        content: str = post.content_field
        user_id: str = user.id_field
        created_at: int = post.created_at_field
        updated_at: int = post.updated_at_field

        class Config:
            title = "UpdatePostResponse.Data"

    data: Data


def handle(
    post_id: int,
    request: UpdatePostRequest,
    current_user: user.User = Depends(GetAuthorizedUser(allowed_roles=[user.Role.ADMIN, user.Role.COMMON])),
) -> UpdatePostResponse:
    with Session(engine) as session:
        post_to_update = session.get(post.Post, post_id)
        if not post_to_update:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        if user.Role(current_user.role) != user.Role.ADMIN and post_to_update.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User does not authorized")
        post_to_update.updated_at = get_current_unix_timestamp()
        updated_data = request.dict(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(post_to_update, key, value)
        session.add(post_to_update)
        session.commit()
        session.refresh(post_to_update)
        return UpdatePostResponse(
            data=UpdatePostResponse.Data(
                id=post_to_update.id,
                title=post_to_update.title,
                content=post_to_update.content,
                user_id=post_to_update.user_id,
                created_at=post_to_update.created_at,
                updated_at=post_to_update.updated_at
            )
        )

