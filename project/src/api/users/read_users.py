from typing import List

from fastapi import Query, Request
from sqlmodel import Session, select, func

from src.api.common import Link, SchemaModel, Pagination, get_links_for_pagination
from src.database import engine
from src.models import user


class ReadUsersResponse(SchemaModel):
    class Data(SchemaModel):
        id: str = user.id_field
        name: str = user.name_field

        class Config:
            title = "ReadUsersResponse.Data"

    pagination: Pagination
    data: List[Data]
    links: List[Link]


def handle(
    *, offset: int = 0, limit: int = Query(default=100, lte=100), request: Request
) -> ReadUsersResponse:
    with Session(engine) as session:
        # get total count of rows for pagination
        statement = select([func.count(user.User.id)])
        total = session.exec(statement).one()

        # get all rows
        statement = select(user.User).order_by(user.User.id).offset(offset).limit(limit)
        results = session.exec(statement)
        users = results.all()
        return ReadUsersResponse(
            pagination=Pagination(offset=offset, limit=limit, total=total),
            data=[
                ReadUsersResponse.Data(
                    id=user_.id,
                    name=user_.name,
                )
                for user_ in users
            ],
            links=get_links_for_pagination(offset, limit, total, request),
        )
