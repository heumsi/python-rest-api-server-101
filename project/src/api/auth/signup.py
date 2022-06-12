from fastapi import HTTPException, status
from sqlmodel import Session

from src.api.auth.utils import get_hashed_password
from src.api.common import SchemaModel
from src.database import engine
from src.models import user


class SignupRequest(SchemaModel):
    id: str = user.id_field
    name: str = user.name_field
    password: str = user.password_field


class SignUpResponse(SchemaModel):
    class Data(SchemaModel):
        id: str = user.id_field
        name: str = user.name_field

        class Config:
            title = "SignUpResponse.Data"

    data: Data


def handle(request: SignupRequest) -> SignUpResponse:
    with Session(engine) as session:
        existing_user = session.get(user.User, request.id)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exist")
        request.password = get_hashed_password(request.password)
        new_user = user.User(
            id=request.id,
            name=request.name,
            password=request.password,
        )
        session.add(new_user)
        session.commit()
        return SignUpResponse(
            data=SignUpResponse.Data(
                id=new_user.id,
                name=new_user.name,
            )
        )
