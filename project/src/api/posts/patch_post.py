from typing import Optional

from fastapi import Depends, HTTPException
from sqlmodel import Session
from starlette import status

from src.api.auth.utils import GetAuthorizedUser
from src.api.common import SchemaModel
from src.database import engine
from src.models import post, user
from src.models.utils import get_current_unix_timestamp


class PatchPostRequest(SchemaModel):
    title: Optional[str] = post.title_field
    content: Optional[str] = post.content_field


class PatchPostResponse(SchemaModel):
    class Data(SchemaModel):
        id: int = post.id_field
        title: str = post.title_field
        content: str = post.content_field
        created_at: int = post.created_at_field
        updated_at: int = post.updated_at_field

        class User(SchemaModel):
            id: str = user.id_field

            class Config:
                title = 'PatchPostResponse.Data.User'

        user: User

        class Config:
            title = 'PatchPostResponse.Data'

    data: Data


def handle(
    post_id: int,
    request: PatchPostRequest,
    current_user: user.User = Depends(GetAuthorizedUser(allowed_roles=[user.Role.ADMIN, user.Role.COMMON])),
) -> PatchPostResponse:
    with Session(engine) as session:
        post_to_patch = session.get(post.Post, post_id)
        if not post_to_patch:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        if user.Role(current_user.role) != user.Role.ADMIN and post_to_patch.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User does not authorized")
        post_to_patch.updated_at = get_current_unix_timestamp()
        updated_data = request.dict(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(post_to_patch, key, value)
        session.add(post_to_patch)
        session.commit()
        session.refresh(post_to_patch)
        return PatchPostResponse(
            data=PatchPostResponse.Data(
                id=post_to_patch.id,
                title=post_to_patch.title,
                content=post_to_patch.content,
                created_at=post_to_patch.created_at,
                updated_at=post_to_patch.updated_at,
                user=PatchPostResponse.Data.User(
                    id=post_to_patch.user_id,
                )
            )
        )
