# 모델 분리하기

현재 모든 엔드포인트에서 `Post` 단일 모델 하나만 사용하고 있습니다.
이 때문에 `Post` 모델을 생성하거나 업데이트할 때, 입력받지 않아도 되는 필드들(`id`, `created_at` 등...)까지 모두 노출되고 있습니다.

`Post` 모델을 필요에 맞게 분리하여 사용할 수 있도록 코드를 수정해봅시다.

## `model.py`

다음과 같이 코드를 수정합니다.

```python{11-14,17-20}
import time
from typing import Optional

from sqlmodel import SQLModel, Field


def get_current_unix_timestamp() -> int:
    return int(time.time())


class PostBase(SQLModel):
    title: str
    author: str
    content: str


class Post(PostBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[int] = Field(default_factory=get_current_unix_timestamp)
    updated_at: Optional[int] = Field(default_factory=get_current_unix_timestamp)
```

## `api.py`

다음과 같이 코드를 수정합니다.

```python{9,20,22,48,53-54}
from typing import List

from fastapi import FastAPI, HTTPException, status, Query
from fastapi.responses import PlainTextResponse
from sqlmodel import Session, select

from src.database import engine, create_db_and_tables
from src.model import Post
from src.model import PostBase, get_current_unix_timestamp

app = FastAPI()


@app.get("/", response_class=PlainTextResponse, status_code=status.HTTP_200_OK)
def healthcheck() -> str:
    return "I'm Alive!"


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post_base: PostBase) -> Post:
    with Session(engine) as session:
        new_post = Post.from_orm(post_base)
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
def update_post(post_id: int, post_base: PostBase) -> Post:
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        post.updated_at = get_current_unix_timestamp()
        updated_post_data = post_base.dict(exclude_unset=True)
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

## 정리

경우에 따라 `Post` 대신 `PostBase` 모델을 사용하여 API에 필요치 않은 모델 필드를 숨겼습니다!
