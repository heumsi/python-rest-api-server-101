from fastapi import status
from sqlmodel import Session

from src.database import engine
from src.models import post


def test_handle_successfully(client, common_user):
    # given
    with Session(engine) as session:
        session.add(post.Post(
            id=1,
            title="테스트 제목",
            user_id=common_user.id,
            user=common_user,
            content="테스트 내용"
        ))
        session.commit()
        session.refresh(common_user)

    # when
    response = client.get(
        "/posts/1",
    )

    # then
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data == {
        "id": 1,
        "title": "테스트 제목",
        "content": "테스트 내용",
        "created_at": data["created_at"],
        "updated_at": data["updated_at"],
        "user_id": common_user.id,
        "user_name": common_user.name,
    }


def test_handle_unsuccessfully_with_not_found(client):
    # when
    response = client.get(
        "/posts/2",
    )

    # then
    assert response.status_code == status.HTTP_404_NOT_FOUND
