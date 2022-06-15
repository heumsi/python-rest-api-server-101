from fastapi import Depends, HTTPException, Response, status
from sqlmodel import Session

from src.api.auth.utils import GetAuthorizedUser
from src.api.common import SchemaModel
from src.database import engine
from src.models import comment, post, user


class CreateCommentReqeust(SchemaModel):
    post_id: int
    content: str = comment.content_field


def handle(
    *,
    request: CreateCommentReqeust,
    current_user: user.User = Depends(
        GetAuthorizedUser(allowed_roles=[user.Role.ADMIN, user.Role.COMMON])
    ),
    response: Response,
) -> None:
    with Session(engine) as session:
        existing_post = session.get(post.Post, request.post_id)
        if not existing_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )
        new_comment = comment.Comment(
            content=request.content,
            user_id=current_user.id,
            post_id=request.post_id,
            user=current_user,
            post=existing_post,
        )
        session.add(new_comment)
        session.commit()
        session.refresh(new_comment)
        response.headers["Location"] = f"/comments/{new_comment.id}"
