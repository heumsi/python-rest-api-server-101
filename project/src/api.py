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



tags = ["user"]


@app.get("/users",
    dependencies=[Depends(GetAuthorizedUser(allowed_roles=[Role.ADMIN]))],
    status_code=status.HTTP_200_OK,
    tags=tags
)
def read_users(offset: int = 0, limit: int = Query(default=100, lte=100)) -> List[UserBase]:
    with Session(engine) as session:
        statement = select(User).offset(offset).limit(limit)
        results = session.exec(statement)
        users = results.all()
        return [user.to_user_base() for user in users]


@app.get("/users/me", tags=tags)
def get_me(user: User = Depends(get_current_user)) -> UserBase:
    return user.to_user_base()


tags = ["post"]


@app.post("/posts", status_code=status.HTTP_201_CREATED, tags=tags)
def create_post(
    post_base: PostBase,
    user: User = Depends(GetAuthorizedUser(allowed_roles=[Role.ADMIN, Role.COMMON]))
) -> Post:
    with Session(engine) as session:
        new_post = Post(
            title=post_base.title,
            content=post_base.content,
            user_id=user.id,
        )
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
        return new_post


@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK, tags=tags)
def read_post(post_id: int) -> Post:
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return post


@app.get("/posts", status_code=status.HTTP_200_OK, tags=tags)
def read_posts(offset: int = 0, limit: int = Query(default=100, lte=100)) -> List[Post]:
    with Session(engine) as session:
        statement = select(Post).offset(offset).limit(limit)
        results = session.exec(statement)
        posts = results.all()
        return posts


@app.put("/posts/{post_id}", status_code=status.HTTP_200_OK, tags=tags)
def update_post(
    post_id: int,
    post_base: PostBase,
    user: User = Depends(GetAuthorizedUser(allowed_roles=[Role.ADMIN, Role.COMMON])),
) -> Post:
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        if Role(user.role) != Role.ADMIN and post.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User does not authorized")
        post.updated_at = get_current_unix_timestamp()
        updated_post_data = post_base.dict(exclude_unset=True)
        for key, value in updated_post_data.items():
            setattr(post, key, value)
        session.add(post)
        session.commit()
        session.refresh(post)
        return post


@app.patch("/posts/{post_id}", status_code=status.HTTP_200_OK, tags=tags)
def path_post(
    post_id: int,
    post_patch: PostPatch,
    user: User = Depends(GetAuthorizedUser(allowed_roles=[Role.ADMIN, Role.COMMON])),
) -> Post:
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        if Role(user.role) != Role.ADMIN and post.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User does not authorized")
        post.updated_at = get_current_unix_timestamp()
        updated_post_data = post_patch.dict(exclude_unset=True)
        for key, value in updated_post_data.items():
            setattr(post, key, value)
        session.add(post)
        session.commit()
        session.refresh(post)
        return post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT, tags=tags)
def delete_post(
    post_id: int,
    user: User = Depends(GetAuthorizedUser(allowed_roles=[Role.ADMIN, Role.COMMON])),
) -> None:
    with Session(engine) as session:
        statement = select(Post).where(Post.id == post_id)
        results = session.exec(statement)
        post = results.first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        if Role(user.role) != Role.ADMIN and post.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User does not authorized")
        session.delete(post)
        session.commit()

