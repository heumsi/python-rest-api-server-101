from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field

from src.models.utils import get_current_unix_timestamp

title_field = Field(description="게시글 제목", min_length=1, max_length=100,)
user_id_field = Field(description="게시글 작성자의 유저 ID", min_length=1, max_length=30)
content_field = Field(description="게시글 내용")
schema_extra = {
    "example": {
        "title": "첫 번째 게시글 입니다!",
        "content": "첫 번째 게시글 내용입니다!"
    }
}


class PostBase(SQLModel):
    title: str = Field(description="게시글 제목", min_length=1, max_length=100)
    content: str = content_field

    class Config:
        schema_extra = schema_extra


class Post(PostBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = user_id_field
    created_at: Optional[int] = Field(default_factory=get_current_unix_timestamp)
    updated_at: Optional[int] = Field(default_factory=get_current_unix_timestamp)


class PostPatch(PostBase):
    title: Optional[str] = title_field
    content: Optional[str] = content_field


id_field = Field(description="유저 아이디", min_length=1, max_length=50, primary_key=True)
name_field = Field(description="유저 이름", min_length=1, max_length=50)
password_field = Field(description="유저 패스워드", min_length=1, )


class UserBase(SQLModel):
    id: str = id_field
    name: str = name_field


class UserSignup(UserBase):
    password: str = password_field


class Role(Enum):
    ADMIN = "ADMIN"
    COMMON = "COMMON"

    def __str__(self) -> str:
        return self.value


class User(SQLModel, table=True):
    id: str = id_field
    name: str = name_field
    password: str = password_field
    role: Optional[str] = Field(description="유저 롤", default=str(Role.COMMON))
    created_at: Optional[int] = Field(default_factory=get_current_unix_timestamp)
    updated_at: Optional[int] = Field(default_factory=get_current_unix_timestamp)

    def to_user_base(self) -> UserBase:
        return UserBase(
            id=self.id,
            name=self.name
        )
