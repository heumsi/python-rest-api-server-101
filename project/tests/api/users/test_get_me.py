from fastapi import status


def test_handle_successfully(client, headers_with_authorized_common):
    # when
    response = client.get(
        "/users/me",
        headers=headers_with_authorized_common
    )

    # then
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": "heumsi",
        "name": "heumsi"
    }


def test_handle_unsuccessfully_with_no_auth(client):
    # when
    response = client.get(
        "/users/me",
    )

    # then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
