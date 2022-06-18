from typing import List

from fastapi import HTTPException, Request, status
from sqlmodel import Session

from src.api.common import Link, SchemaModel
from src.database import engine
from src.models import comment, post, user
from src.models.comment import Comment


class ReadCommentResponse(SchemaModel):
    class Data(SchemaModel):
        id: int = comment.id_field
        content: str = comment.content_field
        created_at: int = comment.created_at_field
        updated_at: int = comment.updated_at_field

        class Post(SchemaModel):
            id: int = post.id_field

            class Config:
                title = "ReadCommentResponse.Data.Post"

        class User(SchemaModel):
            id: str = user.id_field
            name: str = user.name_field

            class Config:
                title = "ReadCommentResponse.Data.User"

        post: Post
        user: User

        links: List[Link]

        class Config:
            title = "ReadCommentResponse.Data"

    data: Data
    links: List[Link]


def handle(comment_id: int, request: Request) -> ReadCommentResponse:
    with Session(engine) as session:
        comment_to_read = session.get(Comment, comment_id)
        if not comment_to_read:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found",
            )
        return ReadCommentResponse(
            data=ReadCommentResponse.Data(
                id=comment_to_read.id,
                content=comment_to_read.content,
                created_at=comment_to_read.created_at,
                updated_at=comment_to_read.updated_at,
                post=ReadCommentResponse.Data.Post(
                    id=comment_to_read.post_id,
                ),
                user=ReadCommentResponse.Data.User(
                    id=comment_to_read.user.id,
                    name=comment_to_read.user.name,
                ),
                links=[
                    Link(
                        rel="self",
                        href=f"{request.base_url}v1/comments/{comment_to_read.id}",
                    ),
                    Link(
                        rel="post",
                        href=f"{request.base_url}v1/posts/{comment_to_read.post_id}",
                    ),
                ],
            ),
            links=[Link(rel="self", href=str(request.url))],
        )
