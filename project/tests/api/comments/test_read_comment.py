from fastapi import status
from sqlmodel import Session

from src.database import engine
from src.models import comment, post


def test_handle_successfully(client, common_user):
    # given
    with Session(engine) as session:
        post_ = post.Post(
            title="테스트 제목",
            user_id=common_user.id,
            content="테스트 내용",
            user=common_user
        )
        comment_ = comment.Comment(
            post_id=post_.id,
            user_id=common_user.id,
            content="테스트 내용",
            user=common_user,
            post=post_
        )
        session.add(post_)
        session.add(comment_)
        session.commit()
        session.refresh(post_)
        session.refresh(comment_)
        session.refresh(common_user)

    # when
    response = client.get(
        f"/comments/{comment_.id}",
    )

    # then
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data == {
        "id": comment_.id,
        "post_id": post_.id,
        "user_id": common_user.id,
        "user_name": common_user.name,
        "content": "테스트 내용",
        "created_at": data["created_at"],
        "updated_at": data["updated_at"],
    }


def test_handle_unsuccessfully_with_not_found(client):
    # when
    response = client.get(
        "/comments/1",
    )

    # then
    assert response.status_code == status.HTTP_404_NOT_FOUND
