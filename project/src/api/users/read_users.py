from typing import List

from fastapi import Query, Request
from pydantic import BaseModel
from sqlmodel import Session, select

from src.api.common import Link
from src.database import engine
from src.models import user


class ReadUsersResponse(BaseModel):
    class Data(BaseModel):
        id: str = user.id_field
        name: str = user.name_field

        class Config:
            title = "ReadUsersResponse.Data"

    data: List[Data]
    links: List[Link]


def handle(*,
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    request: Request
) -> ReadUsersResponse:
    with Session(engine) as session:
        statement = select(user.User).offset(offset).limit(limit)
        results = session.exec(statement)
        users = results.all()
        return ReadUsersResponse(
            data=[
                ReadUsersResponse.Data(
                    id=user_.id,
                    name=user_.name,
                )
                for user_ in users
            ],
            links=[
                Link(
                    rel="self",
                    href=request.url._url,
                )
            ]
        )
