from typing import List

from fastapi import HTTPException, status, Request
from sqlmodel import Session

from src.api.common import Link, SchemaModel
from src.database import engine
from src.models import post, user
from src.models.post import Post


class ReadPostResponse(SchemaModel):
    class Data(SchemaModel):
        id: int = post.id_field
        title: str = post.title_field
        content: str = post.content_field
        created_at: int = post.created_at_field
        updated_at: int = post.updated_at_field

        class User(SchemaModel):
            id: str = user.id_field
            name: str = user.name_field

            class Config:
                title = 'ReadPostResponse.Data.User'

        user: User

        class Config:
            title = 'ReadPostResponse.Data'

    data: Data
    links: List[Link]


def handle(post_id: int, request: Request) -> ReadPostResponse:
    with Session(engine) as session:
        post_to_read = session.get(Post, post_id)
        if not post_to_read:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return ReadPostResponse(
            data=ReadPostResponse.Data(
                id=post_to_read.id,
                title=post_to_read.title,
                content=post_to_read.content,
                created_at=post_to_read.created_at,
                updated_at=post_to_read.updated_at,
                user=ReadPostResponse.Data.User(
                    id=post_to_read.user.id,
                    name=post_to_read.user.name,
                )
            ),
            links=[
                Link(
                    rel="self",
                    href=str(request.url),
                ),
                Link(
                    rel="comments",
                    href=f"{request.base_url}comments?post_id={post_id}"
                ),
                Link(
                    rel="feedbacks",
                    href=f"{request.base_url}feedbacks/posts?post_id={post_id}"
                )
            ]
        )
