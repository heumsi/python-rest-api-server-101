from fastapi import Depends, Response
from sqlmodel import Session

from src.api.auth.utils import GetAuthorizedUser
from src.api.common import SchemaModel
from src.database import engine
from src.models import post, user


class CreatePostReqeust(SchemaModel):
    title: str = post.title_field
    content: str = post.content_field


class CreatePostResponse(SchemaModel):
    class Data(SchemaModel):
        id: int = post.id_field
        title: str = post.title_field
        content: str = post.content_field
        created_at: int = post.created_at_field
        updated_at: int = post.updated_at_field

        class User(SchemaModel):
            id: str = user.id_field

            class Config:
                title = 'CreatePostResponse.Data.User'

        user: User

        class Config:
            title = 'CreatePostResponse.Data'

    data: Data


def handle(
    *,
    request: CreatePostReqeust,
    current_user: user.User = Depends(GetAuthorizedUser(allowed_roles=[user.Role.ADMIN, user.Role.COMMON])),
    response: Response,
) -> CreatePostResponse:
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
        return CreatePostResponse(
            data=CreatePostResponse.Data(
                id=new_post.id,
                title=new_post.title,
                content=new_post.content,
                created_at=new_post.created_at,
                updated_at=new_post.updated_at,
                user=CreatePostResponse.Data.User(
                    id=new_post.user_id
                )
            )
        )
