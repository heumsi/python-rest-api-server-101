from typing import List

from fastapi import Query
from pydantic import BaseModel
from sqlmodel import Session, select

from src.database import engine
from src.models import user


class ReadUsersResponse(BaseModel):
    class Item(BaseModel):
        id: str = user.id_field
        name: str = user.name_field

    items: List[Item]


def handle(offset: int = 0, limit: int = Query(default=100, lte=100)) -> ReadUsersResponse:
    with Session(engine) as session:
        statement = select(user.User).offset(offset).limit(limit)
        results = session.exec(statement)
        users = results.all()
        return ReadUsersResponse(
            items=[ReadUsersResponse.Item(id=user_.id, name=user_.name) for user_ in users]
        )
