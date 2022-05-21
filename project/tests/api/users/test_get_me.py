from fastapi.testclient import TestClient
from fastapi import status

import os
os.environ["DB_URL"] = "sqlite:///:memory:"

from src.api import app


def test_handle_successfully():
    with TestClient(app) as client:
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
            "/users/me",
            headers=headers
        )

        # then
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "id": "heumsi",
            "name": "heumsi"
        }


def test_handle_unsuccessfully_with_no_auth():
    with TestClient(app) as client:
        # when
        response = client.get(
            "/users/me",
        )

        # then
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
