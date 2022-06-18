from fastapi import FastAPI

from src.api import v1
from src.database import create_db_and_tables

app = FastAPI()
app.mount("/v1", v1.app)


@app.on_event("startup")
def handle_startup_event():
    create_db_and_tables()
