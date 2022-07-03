# 모델 메타 데이터 풍성하기 하기

현재 모델 코드를 보면 단순히 변수와 자료 타입만 표현되어 있습니다.
이번에는 모델 속성에 제약사항을 추가하는 등 모델에 여러 메타 데이터를 표현해봅시다.

`model.py` 를 다음처럼 수정합니다.

```python{11-20,24-29,39-41}
import time
from typing import Optional

from sqlmodel import SQLModel, Field


def get_current_unix_timestamp() -> int:
    return int(time.time())


title_field = Field(description="게시글 제목", min_length=1, max_length=100,)
author_field = Field(description="게시글 작성자", min_length=1, max_length=30)
content_field = Field(description="게시글 내용")
schema_extra = {
    "example": {
        "title": "첫 번째 게시글 입니다!",
        "author": "heumsi",
        "content": "첫 번째 게시글 내용입니다!"
    }
}


class PostBase(SQLModel):
    title: str = Field(description="게시글 제목", min_length=1, max_length=100)
    author: str = author_field
    content: str = content_field

    class Config:
        schema_extra = schema_extra


class Post(PostBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[int] = Field(default_factory=get_current_unix_timestamp)
    updated_at: Optional[int] = Field(default_factory=get_current_unix_timestamp)


class PostPatch(PostBase):
    title: Optional[str] = title_field
    author: Optional[str] = author_field
    content: Optional[str] = content_field
```

- `sqlmodel.Field` 의 여러 파라미터를 통해 모델 속성에 제약사항이나 설명을 추가할 수 있습니다.
  - `sqlmodel.Field` 는 `pydantic.Field` 와 호환되므로 파라미터 값에 대한 정보는 [공식 문서](https://pydantic-docs.helpmanual.io/usage/types/)에서 확인하실 수 있습니다.
- 공통으로 쓰이는 변수들은 클래스 밖으로 빼두어서 재사용 가능하도록 했습니다.

이전보다 모델에 대한 정보가 좀 더 풍성해졌습니다!
