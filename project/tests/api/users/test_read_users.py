from fastapi import status


def test_handle_successfully(client, headers_with_authorized_admin):
    # when
    response = client.get(
        "/users/",
        headers=headers_with_authorized_admin
    )

    # then
    assert response.status_code == status.HTTP_200_OK
    json_data = response.json()
    data = json_data.get("data")
    assert data == [
        {
            "id": "admin",
            "name": "admin",
        }
    ]


def test_handle_unsuccessfully_with_no_authentication(client):
    # when
    response = client.get(
        "/users/",
    )

    # then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_handle_unsuccessfully_with_no_authorization(client, headers_with_authorized_common):
    # when
    response = client.get(
        "/users/",
        headers=headers_with_authorized_common
    )

    # then
    assert response.status_code == status.HTTP_403_FORBIDDEN
