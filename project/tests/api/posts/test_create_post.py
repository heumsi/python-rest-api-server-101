from fastapi import status
from sqlmodel import Session, select

from src.database import engine
from src.models import post


def test_handle_successfully(client, headers_with_authorized_common):
    # when
    response = client.post(
        "/posts/",
        headers=headers_with_authorized_common,
        json={
            "title": "테스트 제목",
            "content": "테스트 내용"
        }
    )

    # then
    assert response.status_code == status.HTTP_201_CREATED
    json_data = response.json()
    data = json_data.get("data")
    assert data == {
        "id": data["id"],
        "title": "테스트 제목",
        "content": "테스트 내용",
        "created_at": data["created_at"],
        "updated_at": data["updated_at"],
        "user_id": data["user_id"],
    }
    with Session(engine) as session:
        statement = select(post.Post)
        results = session.exec(statement)
        posts = results.all()
        assert len(posts) == 1
        assert posts[0] == post.Post(
            id=posts[0].id,
            title="테스트 제목",
            content="테스트 내용",
            user_id=posts[0].user_id,
            created_at=posts[0].created_at,
            updated_at=posts[0].updated_at,
        )


def test_handle_unsuccessfully_with_no_auth(client):
    # when
    response = client.post(
        "/posts/",
    )

    # then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
