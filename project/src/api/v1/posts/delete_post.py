from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from src.api.v1.auth.utils import GetAuthorizedUser
from src.database import engine
from src.models.post import Post
from src.models.user import Role, User


def handle(
    post_id: int,
    user: User = Depends(GetAuthorizedUser(allowed_roles=[Role.ADMIN, Role.COMMON])),
) -> None:
    with Session(engine) as session:
        statement = select(Post).where(Post.id == post_id)
        results = session.exec(statement)
        post = results.first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )
        if Role(user.role) != Role.ADMIN and post.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not authorized",
            )
        session.delete(post)
        session.commit()
