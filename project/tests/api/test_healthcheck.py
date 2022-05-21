from fastapi.testclient import TestClient
from fastapi import status

from src.api import app

client = TestClient(app)


def test_handle():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.text == "I'm Alive!"
