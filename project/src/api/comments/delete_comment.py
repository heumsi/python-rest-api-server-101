from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from src.api.auth.utils import GetAuthorizedUser
from src.database import engine
from src.models.comment import Comment
from src.models.user import Role, User


def handle(
    comment_id: int,
    user: User = Depends(GetAuthorizedUser(allowed_roles=[Role.ADMIN, Role.COMMON])),
) -> None:
    with Session(engine) as session:
        statement = select(Comment).where(Comment.id == comment_id)
        results = session.exec(statement)
        comment = results.first()
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found",
            )
        if Role(user.role) != Role.ADMIN and comment.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not authorized",
            )
        session.delete(comment)
        session.commit()
