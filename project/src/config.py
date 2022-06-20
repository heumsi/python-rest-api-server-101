from pydantic import BaseSettings, Field


class DB(BaseSettings):
    url: str = Field(env="DB__SQLALCHEMY_URL")
    echo: bool = Field(env="DB__ECHO")


class Auth(BaseSettings):
    jwt_secret_key: str = Field(env="AUTH__JWT_SECRET_KEY")
    jwt_algorithm: str = Field(env="AUTH__JWT_ALGORITHM")


db = DB()
auth = Auth()
