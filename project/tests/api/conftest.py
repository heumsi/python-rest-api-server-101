import os
from typing import Dict

from src.models.user import User

os.environ["DB_URL"] = "sqlite:///:memory:"

from sqlmodel import Session, SQLModel
import pytest
from fastapi.testclient import TestClient
from fastapi import status

from src.api import app
from src.api.auth.utils import get_hashed_password
from src.database import engine
from src.models import user


@pytest.fixture(scope="session")
def client() -> TestClient:
    with TestClient(app) as client:
        return client


@pytest.fixture()
def common_user() -> user.User:
    with Session(engine) as session:
        user_ = user.User(
            id="heumsi",
            name="heumsi",
            password=get_hashed_password("1234"),
        )
        session.add(user_)
        session.commit()
        session.refresh(user_)
    return user_


@pytest.fixture()
def headers_with_authorized_common(client, common_user) -> Dict[str, str]:
    response = client.post(
        "/auth/signin",
        headers={
            "content-type": "application/x-www-form-urlencoded",
        },
        data={
            "username": common_user.id,
            "password": "1234",
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    headers = {
        "Authorization": f"{data['token_type']} {data['access_token']}"
    }
    return headers


@pytest.fixture()
def headers_with_authorized_common_another(client) -> Dict[str, str]:
    # given
    response = client.post(
        "/auth/signup",
        json={
            "id": "hardy",
            "name": "hardy",
            "password": "1234",
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    response = client.post(
        "/auth/signin",
        headers={
            "content-type": "application/x-www-form-urlencoded",
        },
        data={
            "username": "hardy",
            "password": "1234",
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    headers = {
        "Authorization": f"{data['token_type']} {data['access_token']}"
    }
    return headers


@pytest.fixture()
def headers_with_authorized_admin(client) -> Dict[str, str]:
    # given
    with Session(engine) as session:
        session.add(user.User(
            id="admin", name="admin", password=get_hashed_password("1234"), role=str(user.Role.ADMIN))
        )
        session.commit()

    response = client.post(
        "/auth/signin",
        headers={
            "content-type": "application/x-www-form-urlencoded",
        },
        data={
            "username": "admin",
            "password": "1234",
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    headers = {
        "Authorization": f"{data['token_type']} {data['access_token']}"
    }
    return headers


@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    SQLModel.metadata.create_all(bind=engine)
    yield
    SQLModel.metadata.drop_all(bind=engine)
