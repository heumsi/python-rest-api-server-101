# 프로젝트 생성하기

파이썬 프로젝트를 생성하고, 프로젝트에 필요한 의존성 패키지들을 설치해봅시다. 

## 디렉토리 생성

먼저 프로젝트 디렉토리를 생성하고 진입합니다. 
게시판 관련 프로젝트를 만들 것이기 때문에 이름은 `board_project` 로 짓겠습니다.

```bash
$ mkdir board_project
$ cd board_project
```

## 가상 환경 생성

파이썬 내장 패키지인 `venv` 로 가상환경을 다음 명령어로 생성합니다.

```bash
$ python -m venv .venv
```

실행 이후 다음처럼 `.venv` 디렉토리가 생성된 것을 확인할 수 있습니다.

```bash
$ ls

.venv
```

이제 다음 명령어로 가상 환경에 진입합니다.

```bash
$ source .venv/bin/activate
```

가상 환경에 진입하고 나면 셸 한쪽에 `(.venv)` 와 같은 표시가 등장할 수 있습니다.

## 의존성 패키지 설치

프로젝트에 사용할 패키지를 설치하려고 합니다.
우선 기본적으로 다음 두 패키지를 설치할 것 입니다.

- [fastapi](https://fastapi.tiangolo.com/ko/)
  - REST API 관련 프레임워크입니다. 
- [sqlmodel](https://sqlmodel.tiangolo.com/)
  - Database Model 관련 프레임워크입니다.

다음 명령어로 위 두 패키지를 설치합니다.

```bash
$ pip install "fastapi[all]"  # fastapi에서 제공하는 기타 extra 패키지들도 같이 설치합니다. 
$ pip install sqlmodel
```

