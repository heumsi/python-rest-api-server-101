from typing import List

from fastapi import FastAPI, HTTPException, status, Query, Depends
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from jose.constants import ALGORITHMS
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError
from sqlmodel import Session, select

from src.database import engine, create_db_and_tables
from src.model import Post, PostPatch, User, UserSignup, UserBase, Role
from src.model import PostBase, get_current_unix_timestamp


@app.get("/",
    response_class=PlainTextResponse,
    status_code=status.HTTP_200_OK,
    summary="헬스체크용 엔드포인트 입니다.",
    description="API 서버가 잘 작동하는지 확인합니다.",
    response_description="API 서버가 잘 작동하고 있습니다.",
)
def healthcheck() -> str:
    return "I'm Alive!"
