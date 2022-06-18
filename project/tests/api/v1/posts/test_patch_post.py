import time

from fastapi import status
from sqlmodel import Session, select

from src.database import engine
from src.models import post


def test_handle_successfully(client, common_user, headers_with_authorized_common):
    # given
    with Session(engine) as session:
        session.add(post.Post(id=1, title="테스트 제목", user_id="heumsi", content="테스트 내용"))
        session.commit()
    time.sleep(1)  # wait for making difference between created_at, updated_at

    # when
    response = client.patch(
        "/v1/posts/1",
        json={
            "title": "수정된 테스트 제목",
        },
        headers=headers_with_authorized_common,
    )

    # then
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with Session(engine) as session:
        statement = select(post.Post)
        results = session.exec(statement)
        posts = results.all()
        assert len(posts) == 1
        assert posts[0] == post.Post(
            id=1,
            title="수정된 테스트 제목",
            content="테스트 내용",
            user_id=posts[0].user_id,
            created_at=posts[0].created_at,
            updated_at=posts[0].updated_at,
        )
        assert posts[0].updated_at > posts[0].created_at


def test_handle_unsuccessfully_with_no_authentication(client):
    # given
    with Session(engine) as session:
        session.add(post.Post(id=1, title="테스트 제목", user_id="heumsi", content="테스트 내용"))
        session.commit()

    # when
    response = client.patch(
        "/v1/posts/1",
        json={
            "title": "수정된 테스트 제목",
        },
    )

    # then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_handle_unsuccessfully_with_no_authorization(
    client, headers_with_authorized_common_another
):
    # given
    with Session(engine) as session:
        session.add(post.Post(id=1, title="테스트 제목", user_id="heumsi", content="테스트 내용"))
        session.commit()

    # when
    response = client.patch(
        "/v1/posts/1",
        json={
            "title": "수정된 테스트 제목",
        },
        headers=headers_with_authorized_common_another,
    )

    # then
    assert response.status_code == status.HTTP_403_FORBIDDEN
