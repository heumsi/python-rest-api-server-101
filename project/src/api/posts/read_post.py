from fastapi import HTTPException, status
from sqlmodel import Session

from src.database import engine
from src.model import Post


def handle(post_id: int) -> Post:
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return post
