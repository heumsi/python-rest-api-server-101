
from typing import List

from fastapi import Query
from sqlmodel import Session, select

from src.database import engine
from src.model import Post


def handle(offset: int = 0, limit: int = Query(default=100, lte=100)) -> List[Post]:
    with Session(engine) as session:
        statement = select(Post).offset(offset).limit(limit)
        results = session.exec(statement)
        posts = results.all()
        return posts
