from fastapi import Depends, Response
from sqlmodel import Session

from src.api.auth.utils import GetAuthorizedUser
from src.api.common import SchemaModel
from src.database import engine
from src.models import post, user


class CreatePostReqeust(SchemaModel):
    title: str = post.title_field
    content: str = post.content_field


def handle(
    *,
    request: CreatePostReqeust,
    current_user: user.User = Depends(
        GetAuthorizedUser(allowed_roles=[user.Role.ADMIN, user.Role.COMMON])
    ),
    response: Response,
) -> None:
    with Session(engine) as session:
        new_post = post.Post(
            title=request.title,
            content=request.content,
            user_id=current_user.id,
            user=current_user,
        )
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
        response.headers["Location"] = f"/posts/{new_post.id}"
