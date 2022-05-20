from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session

from src.api.auth.utils import pwd_context
from src.database import engine
from src.models import user


class SignupRequest(BaseModel):
    id: str = user.id_field
    name: str = user.name_field
    password: str = user.password_field


class SignUpResponse(BaseModel):
    id: str = user.id_field
    name: str = user.name_field


def handle(request: SignupRequest) -> SignUpResponse:
    with Session(engine) as session:
        existing_user = session.get(user.User, request.id)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exist")
        request.password = pwd_context.hash(request.password)
        new_user = user.User(
            id=request.id,
            name=request.name,
            password=request.password,
        )
        session.add(new_user)
        session.commit()
        return SignUpResponse(
            id=new_user.id,
            name=new_user.name,
        )
