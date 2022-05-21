import uvicorn
from dotenv import load_dotenv
load_dotenv()

from src.api import app


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
