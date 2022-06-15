from fastapi import status
from sqlmodel import Session, select

from src.database import engine
from src.models import post


def test_handle_successfully(client, headers_with_authorized_common):
    # given
    with Session(engine) as session:
        session.add(post.Post(id=1, title="테스트 제목", user_id="heumsi", content="테스트 내용"))
        session.commit()

    # when
    response = client.delete("/posts/1", headers=headers_with_authorized_common)

    # then
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with Session(engine) as session:
        statement = select(post.Post)
        results = session.exec(statement)
        posts = results.all()
        assert len(posts) == 0


def test_handle_unsuccessfully_with_not_found(client, headers_with_authorized_common):
    # when
    response = client.delete("/posts/2", headers=headers_with_authorized_common)

    # then
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_handle_unsuccessfully_with_no_authentication(client):
    # given
    with Session(engine) as session:
        session.add(post.Post(id=1, title="테스트 제목", user_id="heumsi", content="테스트 내용"))
        session.commit()

    # when
    response = client.delete(
        "/posts/1",
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
    response = client.delete(
        "/posts/1",
        headers=headers_with_authorized_common_another,
    )

    # then
    assert response.status_code == status.HTTP_403_FORBIDDEN
