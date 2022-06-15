from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from src.api.auth.utils import GetAuthorizedUser
from src.database import engine
from src.models.feedbacks.comment_feedback import CommentFeedback
from src.models.user import Role, User


def handle(
    comment_feedback_id: int,
    current_user: User = Depends(
        GetAuthorizedUser(allowed_roles=[Role.ADMIN, Role.COMMON])
    ),
) -> None:
    with Session(engine) as session:
        statement = select(CommentFeedback).where(
            CommentFeedback.id == comment_feedback_id
        )
        results = session.exec(statement)
        comment_feedback = results.first()
        if not comment_feedback:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="CommentFeedback not found",
            )
        if (
            Role(current_user.role) != Role.ADMIN
            and comment_feedback.user_id != current_user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User does not authorized"
            )
        session.delete(comment_feedback)
        session.commit()
