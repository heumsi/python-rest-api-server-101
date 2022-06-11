from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session

from src.database import engine
from src.models import post, user
from src.models.post import Post


class ReadPostResponse(BaseModel):
    class Data(BaseModel):
        id: int = post.id_field
        title: str = post.title_field
        content: str = post.content_field
        user_id: str = user.id_field
        user_name: str = user.name_field
        created_at: int = post.created_at_field
        updated_at: int = post.updated_at_field

        class Config:
            title = 'ReadPostResponse.Data'

    data: Data


def handle(post_id: int) -> ReadPostResponse:
    with Session(engine) as session:
        post_to_read = session.get(Post, post_id)
        if not post_to_read:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return ReadPostResponse(
            data=ReadPostResponse.Data(
                id=post_to_read.id,
                title=post_to_read.title,
                content=post_to_read.content,
                user_id=post_to_read.user.id,
                user_name=post_to_read.user.name,
                created_at=post_to_read.created_at,
                updated_at=post_to_read.updated_at,
            )
        )
