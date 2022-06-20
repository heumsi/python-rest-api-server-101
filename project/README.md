# Python REST API Example

## Preparations

We use poetry as our build system.
If [poetry](https://python-poetry.org/docs/#installation) is not installed, please install it first.

## Installation

```bash
# Install dependencies
$ poetry install

# Activate virtualenv
$ poetry shell
```

## Usage

First, please set environment variables in `.env`.

```bash
$ touch .env
$ vi .env
```

`.env` is following (example)

```
DB__SQLALCHEMY_URL=sqlite:////Users/user/Desktop/heumsi/repos/python-rest-api-server-101/project/database.db
DB__ECHO=False
AUTH__JWT_SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
AUTH__JWT_ALGORITHM=HS256
```

Next, run uvicorn app.

```bash
# Run REST API Server
$ export PYTHONPATH=$(pwd)
$ uvicorn src.main:app
```

## Development

### How to commit

We use commitizen as our commit method.
Please use `$ cz c` for committing, not `$ git commit`.

```bash
# If you want to commit, Please cz(commitizen) command
$ git add .
$ cz c  # Instead of `git commit`
```

When a commit is attempted, pre-commit works,
and commit is completed only when pre-commit works successfully.

### How to add python packages

We use poetry for package installation.
Therefore, if you need to install a package, please install it with the following command.

```bash
# If you want to add python package, Please poetry command
$ poetry add "package name"  # Instead of `pip install`
```

## Other commands

```bash
# Show all commands
$ make
format                         🔧 코드를 포매팅합니다.
lint                           💯 코드를 린팅합니다.
test                           🧪 테스트 코드를 실행합니다.
```
