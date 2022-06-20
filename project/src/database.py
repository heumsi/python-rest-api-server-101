from sqlmodel import SQLModel, create_engine, pool

from src import config

engine = create_engine(
    url=config.db.url,
    echo=config.db.echo,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=pool.StaticPool,
)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
