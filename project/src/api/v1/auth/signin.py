from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic.main import BaseModel
from sqlmodel import Session

from src import config
from src.api.v1.auth.utils import TokenPayload, pwd_context
from src.database import engine
from src.models.user import User


class SigninResponse(BaseModel):
    access_token: str
    token_type: str

    class Config:
        alias_generator = None


def handle(form_data: OAuth2PasswordRequestForm = Depends()) -> SigninResponse:
    with Session(engine) as session:
        user = session.get(User, form_data.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User does not exist",
            )
        if not pwd_context.verify(form_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Password is incorrect",
            )
    token_payload = TokenPayload(user=user)
    jwt_token = jwt.encode(
        token_payload.dict(),
        key=config.auth.jwt_secret_key,
        algorithm=config.auth.jwt_algorithm,
    )
    return SigninResponse(access_token=jwt_token, token_type="Bearer")
