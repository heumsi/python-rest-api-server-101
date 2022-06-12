from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session

from src.api.auth.utils import GetAuthorizedUser
from src.database import engine
from src.models import comment, user, post
from src.models.utils import get_current_unix_timestamp


class UpdateCommentRequest(BaseModel):
    content: str = comment.content_field


class UpdateCommentResponse(BaseModel):
    class Data(BaseModel):
        id: int = comment.id_field
        content: str = comment.content_field
        created_at: int = comment.created_at_field
        updated_at: int = comment.updated_at_field

        class Post(BaseModel):
            id: int = post.id_field

            class Config:
                title = 'UpdateCommentResponse.Data.Post'

        class User(BaseModel):
            id: str = user.id_field
            name: str = user.name_field

            class Config:
                title = 'UpdateCommentResponse.Data.User'

        post: Post
        user: User

        class Config:
            title = 'UpdateCommentResponse.Data'

    data: Data


def handle(
    comment_id: int,
    request: UpdateCommentRequest,
    current_user: user.User = Depends(GetAuthorizedUser(allowed_roles=[user.Role.ADMIN, user.Role.COMMON])),
) -> UpdateCommentResponse:
    with Session(engine) as session:
        comment_to_update = session.get(comment.Comment, comment_id)
        if not comment_to_update:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        if user.Role(current_user.role) != user.Role.ADMIN and comment_to_update.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User does not authorized")
        comment_to_update.updated_at = get_current_unix_timestamp()
        updated_data = request.dict(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(comment_to_update, key, value)
        session.add(comment_to_update)
        session.commit()
        session.refresh(comment_to_update)
        return UpdateCommentResponse(
            data=UpdateCommentResponse.Data(
                id=comment_to_update.id,
                content=comment_to_update.content,
                created_at=comment_to_update.created_at,
                updated_at=comment_to_update.updated_at,
                post=UpdateCommentResponse.Data.Post(
                    id=comment_to_update.post_id,
                ),
                user=UpdateCommentResponse.Data.User(
                    id=comment_to_update.user.id,
                    name=comment_to_update.user.name,
                ),
            )
        )

