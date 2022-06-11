from typing import List

from fastapi import Query
from pydantic import BaseModel
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from src.database import engine
from src.models import post, user


class ReadPostsResponse(BaseModel):
    class Data(BaseModel):
        id: int = post.id_field
        title: str = post.title_field
        content: str = post.content_field
        user_id: str = user.id_field
        user_name: str = user.name_field
        created_at: int = post.created_at_field
        updated_at: int = post.updated_at_field
        num_likes: int
        num_dislikes: int
        num_comments: int

        class Config:
            title = "ReadPostsResponse.Data"

    data: List[Data]


def handle(offset: int = 0, limit: int = Query(default=100, lte=100)) -> ReadPostsResponse:
    with Session(engine) as session:
        statement = (
            select(post.Post).offset(offset).limit(limit)
            .options(
                selectinload(post.Post.user),
                selectinload(post.Post.comments),
                selectinload(post.Post.feedbacks)
            )
        )
        results = session.exec(statement)
        posts_to_read = results.all()
        return ReadPostsResponse(
            data=[
                ReadPostsResponse.Data(
                    id=post_to_read.id,
                    title=post_to_read.title,
                    content=post_to_read.content,
                    user_id=post_to_read.user_id,
                    user_name=post_to_read.user.name,
                    created_at=post_to_read.created_at,
                    updated_at=post_to_read.updated_at,
                    num_likes=len([feedback for feedback in post_to_read.feedbacks if feedback.like]),
                    num_dislikes=len([feedback for feedback in post_to_read.feedbacks if not feedback.like]),
                    num_comments=len(post_to_read.comments)
                )
                for post_to_read in posts_to_read
            ]
        )
