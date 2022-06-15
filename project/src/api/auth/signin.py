from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlmodel import Session

from src.api.auth.utils import pwd_context, JWT_SECRET_KEY, JWT_ALGORITHM, TokenPayload
from src.api.common import SchemaModel
from src.database import engine
from src.models.user import User


class SigninResponse(SchemaModel):
    class Data(SchemaModel):
        access_token: str
        token_type: str

        class Config:
            title = "SigninResponse.Data"

    data: Data


def handle(form_data: OAuth2PasswordRequestForm = Depends()) -> SigninResponse:
    with Session(engine) as session:
        user = session.get(User, form_data.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not exist"
            )
        if not pwd_context.verify(form_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is incorrect"
            )
    token_payload = TokenPayload(user=user)
    jwt_token = jwt.encode(
        token_payload.dict(), key=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM
    )
    return SigninResponse(
        data=SigninResponse.Data(access_token=jwt_token, token_type="Bearer")
    )
