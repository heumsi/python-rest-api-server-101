from typing import List

from fastapi import Query, Request
from sqlmodel import Session, func, select

from src.api.common import Link, Pagination, SchemaModel, get_links_for_pagination
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


def _get_total(session: Session) -> int:
    """ get total count of rows for pagination """
    statement = select([func.count(user.User.id)])
    return session.exec(statement).one()  # type: ignore


def _get_users(session: Session, offset: int, limit: int) -> List[user.User]:
    """ get all rows """
    statement = select(user.User).order_by(user.User.id).offset(offset).limit(limit)
    results = session.exec(statement)
    return results.all()


def handle(
    *, offset: int = 0, limit: int = Query(default=100, lte=100), request: Request
) -> ReadUsersResponse:
    with Session(engine) as session:
        total = _get_total(session)
        users_to_read = _get_users(session, offset, limit)
        return ReadUsersResponse(
            pagination=Pagination(offset=offset, limit=limit, total=total),
            data=[
                ReadUsersResponse.Data(
                    id=user_.id,
                    name=user_.name,
                )
                for user_ in users_to_read
            ],
            links=get_links_for_pagination(offset, limit, total, request),
        )
