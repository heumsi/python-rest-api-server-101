from typing import List

from fastapi import Depends, Request
from pydantic import BaseModel

from src.api.auth.utils import get_current_user
from src.api.common import Link
from src.models import user


class GetMeResponse(BaseModel):
    class Data(BaseModel):
        id: str = user.id_field
        name: str = user.name_field

        class Config:
            title = "GetMeResponse.Data"

    data: Data
    links: List[Link]


def handle(
    *,
    current_user: user.User = Depends(get_current_user),
    request: Request
) -> GetMeResponse:
    return GetMeResponse(
        data=GetMeResponse.Data(
            id=current_user.id,
            name=current_user.name
        ),
        links=[
            Link(
                rel="self",
                href=request.url._url
            )
        ]
    )
