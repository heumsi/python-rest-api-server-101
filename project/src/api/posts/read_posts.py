from typing import List

from fastapi import Query
from pydantic import BaseModel
from sqlmodel import Session, select

from src.api.posts.read_post import ReadPostResponse
from src.database import engine
from src.models import post


class ReadPostsResponse(BaseModel):
    items: List[ReadPostResponse]


def handle(offset: int = 0, limit: int = Query(default=100, lte=100)) -> ReadPostsResponse:
    with Session(engine) as session:
        statement = select(post.Post).offset(offset).limit(limit)
        results = session.exec(statement)
        posts_to_read = results.all()
        return ReadPostsResponse(
            items=[
                ReadPostResponse(
                    id=post_to_read.id,
                    title=post_to_read.title,
                    content=post_to_read.content,
                    user_id=post_to_read.user_id,
                    user_name=post_to_read.user.name,
                    created_at=post_to_read.created_at,
                    updated_at=post_to_read.updated_at,
                )
                for post_to_read in posts_to_read
            ]
        )
