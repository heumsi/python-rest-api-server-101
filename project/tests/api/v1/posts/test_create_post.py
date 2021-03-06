from fastapi import status
from sqlmodel import Session, select

from src.database import engine
from src.models import post


def test_handle_successfully(client, common_user, headers_with_authorized_common):
    # when
    response = client.post(
        "/v1/posts/",
        headers=headers_with_authorized_common,
        json={"title": "테스트 제목", "content": "테스트 내용"},
    )

    # then
    assert response.status_code == status.HTTP_201_CREATED
    assert response.headers.get("Location").startswith("/v1/posts/")
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
        "/v1/posts/",
    )

    # then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
