from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel

from src.models.utils import get_current_unix_timestamp

id_field = Field(description="유저 아이디", min_length=1, max_length=50, primary_key=True)
name_field = Field(description="유저 이름", min_length=1, max_length=50)
password_field = Field(description="유저 패스워드", min_length=1)


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
