from fastapi import FastAPI

from src.api import auth
from src.database import create_db_and_tables

app = FastAPI(
    title="Project REST API Docs",
    description="프로젝트 REST API 문서입니다.",
    version="v1",
)

app.include_router(auth.router)


@app.on_event("startup")
def handle_startup_event():
    create_db_and_tables()