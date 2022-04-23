# FastAPI 인스턴스 만들기

## FastAPI 인스턴스 생성

서버 역할을 담당할 FastAPI 인스턴스를 생성하는 코드를 다음처럼 `app.py` 에 작성합니다.

```python
from fastapi import FastAPI

app = FastAPI()
```

## 서버 실행 시 이벤트 핸들러 작성

`app` 인스턴스가 서버로 기동될 때, `"startup"` 이라는 이벤트가 발생합니다.
이 떄 Database와 Table도 같이 생성될 수 있도록 `create_db_and_tables()` 함수도 호출해주는 코드를 추가합니다.

```python
@app.on_event("startup")
def handle_startup_event():
    create_db_and_tables()
```

## main 함수 작성

`app.py` 를 실행했을 때 서버가 실행될 수 있도록 다음 코드도 추가해줍니다.  

```python
import uvicorn

def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
```

## 정리

지금까지 `app.py` 에 작성한 코드는 다음과 같습니다. (하이라이팅된 부분은 이번 내용을 통해 추가된 부분입니다.)

```python{28-43}
# app.py

import time
from typing import Optional

from sqlmodel import Field, SQLModel, create_engine

def get_current_unix_timestamp() -> int:
    return int(time.time())

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str
    content: str
    created_at: Optional[int] = Field(default_factory=get_current_unix_timestamp)
    updated_at: Optional[int] = Field(default_factory=get_current_unix_timestamp)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

from fastapi import FastAPI    

app = FastAPI()

import uvicorn

@app.on_event("startup")
def handle_startup_event():
    create_db_and_tables()

def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
```

## 서버 실행

이제 터미널에서 다음 명령어로 `app.py` 를 실행합니다.

```bash
$ python app.py 

INFO:     Started server process [31787]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

서버가 잘 실행되었습니다.

:::tip
위처럼 `python app.py` 명령어로 실행해도 되지만, 다음처럼 `uvicorn` 을 이용해서 실행할 수 있습니다.

```bash
# uvicorn {모듈 명}:{FastAPI Instance 변수 이름}
uvicorn app:app --host "0.0.0.0" --port 8000  
```

이 때 뒤에 `--reload` 옵션을 추가로 설정해주면, 코드 수정 시 코드를 반영하여 서버가 자동으로 재실행 됩니다.
```bash
uvicorn app:app --host "0.0.0.0" --port 8000 --reload
```

실습할 때는 `--reload` 옵션을 주어서 실행하는게 더 편할 거라 생각합니다.
:::