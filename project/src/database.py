import os

from sqlmodel import SQLModel, create_engine, pool

sqlite_url = os.getenv("DB_URL")
if not sqlite_url:
    raise EnvironmentError(f"Please fill os environment: DB_URL")

engine = create_engine(
    sqlite_url,
    echo=True,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=pool.StaticPool,
)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
