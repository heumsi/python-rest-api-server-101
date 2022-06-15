from fastapi import status
from sqlmodel import Session, select

from src.database import engine
from src.models import comment, post


def test_handle_successfully(client, common_user, headers_with_authorized_common):
    # given
    with Session(engine) as session:
        post_ = post.Post(
            title="테스트 제목", user_id=common_user.id, user=common_user, content="테스트 내용"
        )
        session.add(post_)
        session.commit()
        session.refresh(post_)
        session.refresh(common_user)

    # when
    response = client.post(
        "/comments/",
        headers=headers_with_authorized_common,
        json={"post_id": post_.id, "content": "테스트 내용"},
    )

    # then
    assert response.status_code == status.HTTP_201_CREATED
    assert response.headers.get("Location").startswith("/comments/")
    with Session(engine) as session:
        statement = select(comment.Comment)
        results = session.exec(statement)
        comments = results.all()
        assert len(comments) == 1
        assert comments[0] == comment.Comment(
            id=comments[0].id,
            post_id=post_.id,
            content="테스트 내용",
            user_id=comments[0].user_id,
            created_at=comments[0].created_at,
            updated_at=comments[0].updated_at,
        )


def test_handle_unsuccessfully_with_no_auth(client):
    # when
    response = client.post("/comments/", json={"post_id": 1, "content": "테스트 내용"})

    # then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_handle_unsuccessfully_with_not_found_post(
    client, headers_with_authorized_common
):
    # when
    response = client.post(
        "/comments/",
        headers=headers_with_authorized_common,
        json={"post_id": 1, "content": "테스트 내용"},  # not existing post
    )

    # then
    assert response.status_code == status.HTTP_404_NOT_FOUND
