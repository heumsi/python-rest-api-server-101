from typing import List

from fastapi import Query, Request
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select, func

from src.api.common import Link, SchemaModel, Pagination, get_links_for_pagination
from src.database import engine
from src.models import post, user


class ReadPostsResponse(SchemaModel):
    class Data(SchemaModel):
        id: int = post.id_field
        title: str = post.title_field
        content: str = post.content_field
        created_at: int = post.created_at_field
        updated_at: int = post.updated_at_field
        links: List[Link]

        class User(SchemaModel):
            id: str = user.id_field
            name: str = user.name_field

            class Config:
                title = "ReadPostsResponse.Data.User"

        class NumOf(SchemaModel):
            likes: int
            dislikes: int
            comments: int

            class Config:
                title = "ReadPostsResponse.Data.NumOf"

        user: User
        num_of: NumOf

        class Config:
            title = "ReadPostsResponse.Data"

    pagination: Pagination
    data: List[Data]
    links: List[Link]


def handle(
    *, offset: int = 0, limit: int = Query(default=100, lte=100), request: Request
) -> ReadPostsResponse:
    with Session(engine) as session:
        # get total count of rows for pagination
        statement = select([func.count(post.Post.id)])
        total = session.exec(statement).one()

        # get all rows
        statement = (
            select(post.Post)
            .order_by(post.Post.id)
            .offset(offset)
            .limit(limit)
            .options(
                selectinload(post.Post.user),
                selectinload(post.Post.comments),
                selectinload(post.Post.feedbacks),
            )
        )
        results = session.exec(statement)
        posts_to_read = results.all()
        return ReadPostsResponse(
            pagination=Pagination(offset=offset, limit=limit, total=total),
            data=[
                ReadPostsResponse.Data(
                    id=post_to_read.id,
                    title=post_to_read.title,
                    content=post_to_read.content,
                    created_at=post_to_read.created_at,
                    updated_at=post_to_read.updated_at,
                    user=ReadPostsResponse.Data.User(
                        id=post_to_read.user.id,
                        name=post_to_read.user.name,
                    ),
                    num_of=ReadPostsResponse.Data.NumOf(
                        likes=len(
                            [
                                feedback
                                for feedback in post_to_read.feedbacks
                                if feedback.like
                            ]
                        ),
                        dislikes=len(
                            [
                                feedback
                                for feedback in post_to_read.feedbacks
                                if not feedback.like
                            ]
                        ),
                        comments=len(post_to_read.comments),
                    ),
                    links=[
                        Link(
                            rel="self",
                            href=f"{request.base_url}posts/{post_to_read.id}",
                        ),
                        Link(
                            rel="comments",
                            href=f"{request.base_url}comments?post_id={post_to_read.id}",
                        ),
                        Link(
                            rel="feedbacks",
                            href=f"{request.base_url}feedbacks/posts?post_id={post_to_read.id}",
                        ),
                    ],
                )
                for post_to_read in posts_to_read
            ],
            links=get_links_for_pagination(offset, limit, total, request),
        )
