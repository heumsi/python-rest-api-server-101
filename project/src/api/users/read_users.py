from typing import List

from fastapi import Query
from sqlmodel import Session, select

from src.database import engine
from src.models.user import UserBase, User

tags = ["user"]


def handle(offset: int = 0, limit: int = Query(default=100, lte=100)) -> List[UserBase]:
    with Session(engine) as session:
        statement = select(User).offset(offset).limit(limit)
        results = session.exec(statement)
        users = results.all()
        return [user.to_user_base() for user in users]
