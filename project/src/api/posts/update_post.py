from fastapi import Depends, HTTPException
from sqlmodel import Session
from starlette import status

from src.api.auth.utils import GetAuthorizedUser
from src.database import engine
from src.model import User, Role
from src.models.post import PostBase, Post
from src.models.utils import get_current_unix_timestamp


def handle(
    post_id: int,
    post_base: PostBase,
    user: User = Depends(GetAuthorizedUser(allowed_roles=[Role.ADMIN, Role.COMMON])),
) -> Post:
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        if Role(user.role) != Role.ADMIN and post.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User does not authorized")
        post.updated_at = get_current_unix_timestamp()
        updated_post_data = post_base.dict(exclude_unset=True)
        for key, value in updated_post_data.items():
            setattr(post, key, value)
        session.add(post)
        session.commit()
        session.refresh(post)
        return post