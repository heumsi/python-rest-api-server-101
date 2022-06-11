from fastapi import Depends
from pydantic import BaseModel

from src.api.auth.utils import get_current_user
from src.models import user


class GetMeResponse(BaseModel):
    class Data(BaseModel):
        id: str = user.id_field
        name: str = user.name_field

        class Config:
            title = "GetMeResponse.Data"

    data: Data


def handle(current_user: user.User = Depends(get_current_user)) -> GetMeResponse:
    return GetMeResponse(
        data=GetMeResponse.Data(
            id=current_user.id,
            name=current_user.name
        )
    )
