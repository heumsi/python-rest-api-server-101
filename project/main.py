import uvicorn

from project.database import create_db_and_tables


def main() -> None:
    create_db_and_tables()
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
