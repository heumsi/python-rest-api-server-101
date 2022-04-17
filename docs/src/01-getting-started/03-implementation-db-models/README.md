# Database 모델 구현하기

Database의 모델을 구현해봅시다.

## Post 모델 정의하기

게시글 데이터를 담을 모델을 `Post` 모델이라 합시다.
이 안에는 다음과 같은 내용들이 들어가게 됩니다.

- 게시글 제목
- 게시글 작성자
- 게시글 내용
- 게시글 생성 일시
- 게시글 수정 일시

`app.py` 를 만든 뒤 다음 코드를 입력합니다.

```python
import time
from typing import Optional

from sqlmodel import Field, SQLModel

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str
    content: str
    created_at: Optional[int] = Field(default_factory=time.time)
    updated_at: Optional[int] = Field(default_factory=time.time)
```

주요 포인트를 하나씩 살펴보겠습니다.

```python{4,6}
import time
from typing import Optional

from sqlmodel import Field, SQLModel

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str
    content: str
    created_at: Optional[int] = Field(default_factory=time.time)
    updated_at: Optional[int] = Field(default_factory=time.time)
```

- 모델은 클래스로 정의하며, 이 클래스는 `sqlmodel.SQLModel` 클래스를 상속받아야 합니다. 여기서는 `Post` 가 되겠습니다. 
- `table=True` 옵션을 주면, 이 모델은 Database의 Table로도 생성됩니다.
  - Table 이름은 기본적으로 클래스 이름을 `snake_case` 한 형태로 생성되며, 여기서는 `post` 가 됩니다.

```python{1-2,7-12}
import time
from typing import Optional

from sqlmodel import Field, SQLModel

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str
    content: str
    created_at: Optional[int] = Field(default_factory=time.time)
    updated_at: Optional[int] = Field(default_factory=time.time)
```

- `7-12` 라인은 모델이 가지는 속성을 표현합니다. 구체적으로 모델이 담을 데이터 포맷이라고 볼 수 있습니다.
- `table=True` 옵션으로 인해 이 모델은 곧 Database의 Table이기도 합니다, 각각의 속성은 Table의 Column이 됩니다.

## Database와 연동하기

위 `Post` 모델을 실제로 Database와 연동하는 코드를 넣어봅시다.

다음 코드를 추가합니다.

```python
from sqlmodel import SQLModel, create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
```

주요 포인트를 하나씩 살펴보겠습니다.

```python{1,3-6}
from sqlmodel import SQLModel, create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
```

- 여기서는 Database로 File로 간단히 데이터를 저장할 수 있는 SQLite를 사용할 계획입니다.
- `sqlite_file_name` 변수에 SQLite에서 데이터를 담을 파일 이름을 지정합니다.
- `sqlite_url` 변수에는 Database URL을 지정합니다.
- `engine` 변수에 Database와 상호작용을 할 객체인 `Engine`을 담아둡니다.

:::tip
`sqlite_url` 에 표현된 Database URL은 SQLAlchemy에서 사용하는 Database URL 포맷으로, 
많은 Database 관련 프레임워크에서 이 포맷을 사용하곤 합니다.

더 궁금하시다면 [SQLAlchemy 공식 문서](https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls)를 참고하시면 좋습니다.
:::

```python{1,9-10}
from sqlmodel import SQLModel, create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
```

- `9-10` 라인의 함수가 실행되면 `SQLModel` 을 상속받은 모든 클래스가 테이블로 등록됩니다.
  - 위에서 `Post` 클래스가 `SQLModel` 을 상속받았으니, Database에 `post` Table이 이 때 생성됩니다.
  - 만약 `post` Table이 이미 존재한다면 별도로 생성하지 않습니다.

## 정리

지금까지 `app.py` 에 작성한 코드는 다음과 같습니다.

```python
# app.py

import time
from typing import Optional

from sqlmodel import Field, SQLModel, create_engine

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str
    content: str
    created_at: Optional[int] = Field(default_factory=time.time)
    updated_at: Optional[int] = Field(default_factory=time.time)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
```