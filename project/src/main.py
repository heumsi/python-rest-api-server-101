import uvicorn

from src.api import app
from src.database import create_db_and_tables


def main() -> None:
    create_db_and_tables()
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
