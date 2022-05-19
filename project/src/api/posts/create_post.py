# @app.post("/posts", status_code=status.HTTP_201_CREATED, tags=tags)
from fastapi import Depends
from sqlmodel import Session

from src.api.auth.utils import GetAuthorizedUser
from src.database import engine
from src.model import PostBase, User, Role, Post


def handle(
    post_base: PostBase,
    user: User = Depends(GetAuthorizedUser(allowed_roles=[Role.ADMIN, Role.COMMON]))
) -> Post:
    with Session(engine) as session:
        new_post = Post(
            title=post_base.title,
            content=post_base.content,
            user_id=user.id,
        )
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
        return new_post
