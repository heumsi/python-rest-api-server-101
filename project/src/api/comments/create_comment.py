from fastapi import Depends, status, HTTPException, Response
from sqlmodel import Session

from src.api.auth.utils import GetAuthorizedUser
from src.api.common import SchemaModel
from src.database import engine
from src.models import comment, user, post


class CreateCommentReqeust(SchemaModel):
    post_id: int
    content: str = comment.content_field


class CreateCommentResponse(SchemaModel):
    class Data(SchemaModel):
        id: int = comment.id_field
        content: str = comment.content_field
        created_at: int = comment.created_at_field
        updated_at: int = comment.updated_at_field

        class Post(SchemaModel):
            id: int = post.id_field

            class Config:
                title = 'CreateCommentResponse.Data.Post'

        class User(SchemaModel):
            id: str = user.id_field

            class Config:
                title = 'CreateCommentResponse.Data.User'

        post: Post
        user: User

        class Config:
            title = 'CreateCommentResponse.Data'

    data: Data


def handle(
    *,
    request: CreateCommentReqeust,
    current_user: user.User = Depends(GetAuthorizedUser(allowed_roles=[user.Role.ADMIN, user.Role.COMMON])),
    response: Response
) -> CreateCommentResponse:
    with Session(engine) as session:
        existing_post = session.get(post.Post, request.post_id)
        if not existing_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        new_comment = comment.Comment(
            content=request.content,
            user_id=current_user.id,
            post_id=request.post_id,
            user=current_user,
            post=existing_post
        )
        session.add(new_comment)
        session.commit()
        session.refresh(new_comment)
        response.headers["Location"] = f"/comments/{new_comment.id}"
        return CreateCommentResponse(
            data=CreateCommentResponse.Data(
                id=new_comment.id,
                content=new_comment.content,
                post=CreateCommentResponse.Data.Post(id=new_comment.post_id),
                user=CreateCommentResponse.Data.User(id=new_comment.user_id),
                created_at=new_comment.created_at,
                updated_at=new_comment.updated_at
            )
        )
