from fastapi import status


def test_handle(client):
    response = client.get("/v1/")
    assert response.status_code == status.HTTP_200_OK
    assert response.text == "I'm Alive!"
