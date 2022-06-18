from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from src.api.auth.utils import GetAuthorizedUser
from src.api.common import SchemaModel
from src.database import engine
from src.models import comment, user
from src.models.utils import get_current_unix_timestamp


class UpdateCommentRequest(SchemaModel):
    content: str = comment.content_field


def handle(
    comment_id: int,
    request: UpdateCommentRequest,
    current_user: user.User = Depends(
        GetAuthorizedUser(allowed_roles=[user.Role.ADMIN, user.Role.COMMON])
    ),
) -> None:
    with Session(engine) as session:
        comment_to_update = session.get(comment.Comment, comment_id)
        if not comment_to_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found",
            )
        if (
            user.Role(current_user.role) != user.Role.ADMIN
            and comment_to_update.user_id != current_user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not authorized",
            )
        comment_to_update.updated_at = get_current_unix_timestamp()
        updated_data = request.dict(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(comment_to_update, key, value)
        session.add(comment_to_update)
        session.commit()
        session.refresh(comment_to_update)
