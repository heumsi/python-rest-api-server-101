from typing import List

from fastapi import Query
from pydantic import BaseModel
from sqlmodel import Session, select

from src.database import engine
from src.models import user


class ReadUsersResponse(BaseModel):
    class Data(BaseModel):
        id: str = user.id_field
        name: str = user.name_field

        class Config:
            title = "ReadUsersResponse.Data"

    data: List[Data]


def handle(offset: int = 0, limit: int = Query(default=100, lte=100)) -> ReadUsersResponse:
    with Session(engine) as session:
        statement = select(user.User).offset(offset).limit(limit)
        results = session.exec(statement)
        users = results.all()
        return ReadUsersResponse(
            data=[
                ReadUsersResponse.Data(
                    id=user_.id,
                    name=user_.name
                )
                for user_ in users
            ]
        )
