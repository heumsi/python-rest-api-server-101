from fastapi import status
from sqlmodel import Session

from src.database import engine
from src.models import user
from src.api.auth.utils import get_hashed_password


def test_handle_successfully(client):
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

    # when
    response = client.get(
        "/users/",
        headers=headers
    )

    # then
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "items": [
            {
                "id": "admin",
                "name": "admin",
            }
        ]
    }


def test_handle_unsuccessfully_with_no_authentication(client):
    # when
    response = client.get(
        "/users/",
    )

    # then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_handle_unsuccessfully_with_no_authorization(client):
    # given
    response = client.post(
        "/auth/signup",
        json={
            "id": "heumsi",
            "name": "heumsi",
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
            "username": "heumsi",
            "password": "1234",
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    headers = {
        "Authorization": f"{data['token_type']} {data['access_token']}"
    }

    # when
    response = client.get(
        "/users/",
        headers=headers
    )

    # then
    assert response.status_code == status.HTTP_403_FORBIDDEN
