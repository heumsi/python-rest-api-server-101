from typing import List

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from jose.constants import ALGORITHMS
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlmodel import Session

from src.api.common import SchemaModel
from src.database import engine
from src.models.user import Role, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/signin")

JWT_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
JWT_ALGORITHM = ALGORITHMS.HS256


class TokenPayload(SchemaModel):
    user: User


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        token_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        token_payload = TokenPayload(**token_payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is not valid",
        )
    with Session(engine) as session:
        user = session.get(User, token_payload.user.id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User does not exist",
            )
    return user


class GetAuthorizedUser:
    def __init__(self, allowed_roles: List[Role]) -> None:
        self._allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)) -> User:
        if Role(user.role) not in self._allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User does not authorized"
            )
        return user


def get_hashed_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)
