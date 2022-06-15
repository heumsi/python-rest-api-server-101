from fastapi import status



def test_handle(client):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.text == "I'm Alive!"
