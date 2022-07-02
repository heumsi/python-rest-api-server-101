# Layered Architecture로 리팩토링하기

현재 코드가 작성된 하나의 파일을 각 역할에 맞게 여러 파일로 나누어봅시다.
역할에 맞게 나누는 작업을 보통 "레이어링" 이라고 부르는데, 이런 구조로 아키텍처를 만드는 것을 "레이어드 아키텍처" 라고 합니다.

## `src` 디렉토리

앞으로 모든 소스 코드는 `src` 라는 디렉토리에 담을겁니다. `src` 는 `source` 의 약자로, 이렇게 줄여서 표현하곤합니다.

먼저 다음처럼 `src` 디렉토리를 만듭니다.

```bash
$ mkdir src
```

그리고 `main.py` 를 이 안으로 옮깁니다.

```bash
$ mv main.py src/main.py
```

## `main.py` 분리

크게 4개의 모듈을 만들겁니다. 그리고 각 모듈이 담는 의미는 다음과 같습니다.

- `api.py` : 클라이언트에게 제공하는 API에 대한 코드를 담습니다.
- `database.py` : API에서 사용하는 Database에 대한 코드를 담습니다.
- `model.py` : API에서 사용하는 데이터 모델에 대한 코드를 담습니다.
- `main.py` : 서버를 실행하는 코드를 담습니다. 프로젝트 진입점이기도 합니다.

그럼 이제 `main.py` 에 있는 코드를 각 모듈에 다음처럼 나눠봅시다.

### `api.py`

API와 관련된 모든 코드는 이 모듈이 담도록 분리합니다.

```python
from typing import List

from fastapi import FastAPI, HTTPException, status, Query
from fastapi.responses import PlainTextResponse
from sqlmodel import Session, select

from src.database import engine, create_db_and_tables
from src.model import Post

app = FastAPI()


@app.get("/", response_class=PlainTextResponse, status_code=status.HTTP_200_OK)
def healthcheck() -> str:
    return "I'm Alive!"


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post) -> Post:
    with Session(engine) as session:
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
        return new_post


@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
def read_post(post_id: int) -> Post:
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post


@app.get("/posts", status_code=status.HTTP_200_OK)
def read_posts(offset: int = 0, limit: int = Query(default=100, lte=100)) -> List[Post]:
    with Session(engine) as session:
        statement = select(Post).offset(offset).limit(limit)
        results = session.exec(statement)
        posts = results.all()
        return posts


@app.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
def update_post(post_id: int, updated_post: Post) -> Post:
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        post.updated_at = int(time.time())
        updated_post_data = updated_post.dict(exclude_unset=True)
        for key, value in updated_post_data.items():
            setattr(post, key, value)
        session.add(post)
        session.commit()
        session.refresh(post)
        return post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int) -> None:
    with Session(engine) as session:
        statement = select(Post).where(Post.id == post_id)
        results = session.exec(statement)
        post = results.first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        session.delete(post)
        session.commit()


@app.on_event("startup")
def handle_startup_event():
    create_db_and_tables()
```

### `database.py`

Database와 관련된 모든 코드는 이 모듈이 담도록 분리합니다.

```python
from sqlmodel import create_engine, SQLModel

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
```

### `model.py`

데이터 모델과 관련된 모든 코드는 이 모듈이 담도록 분리합니다.

```python
import time
from typing import Optional

from sqlmodel import SQLModel, Field


def get_current_unix_timestamp() -> int:
    return int(time.time())


class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str
    content: str
    created_at: Optional[int] = Field(default_factory=get_current_unix_timestamp)
    updated_at: Optional[int] = Field(default_factory=get_current_unix_timestamp)
```

### `main.py`

서버 실행 및 셋업 관련된 모든 코드는 이 모듈이 담도록 분리합니다.

```python
import uvicorn

from src.api import app


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
```

## 정리

코드의 각 역할에 따라 다음과 같이 코드 나누기를 완료했습니다!

```bash
# as-is
project/
  main.py

# to-be
project/
  src/
    api.py
    database.py
    model.py
    main.py
```

구조가 이전보다 조금 복잡해지기지는 했지만, 훨씬 더 명확하고 확장성 있어 보입니다.
