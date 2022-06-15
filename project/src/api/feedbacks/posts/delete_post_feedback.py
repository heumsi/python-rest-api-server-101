from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from src.api.auth.utils import GetAuthorizedUser
from src.database import engine
from src.models.feedbacks.post_feedback import PostFeedback
from src.models.user import Role, User


def handle(
    post_feedback_id: int,
    current_user: User = Depends(
        GetAuthorizedUser(allowed_roles=[Role.ADMIN, Role.COMMON])
    ),
) -> None:
    with Session(engine) as session:
        statement = select(PostFeedback).where(PostFeedback.id == post_feedback_id)
        results = session.exec(statement)
        post_feedback = results.first()
        if not post_feedback:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="PostFeedback not found"
            )
        if (
            Role(current_user.role) != Role.ADMIN
            and post_feedback.user_id != current_user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User does not authorized"
            )
        session.delete(post_feedback)
        session.commit()
