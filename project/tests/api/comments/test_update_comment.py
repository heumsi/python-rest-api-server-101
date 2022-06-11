import time

from fastapi import status
from sqlmodel import Session, select

from src.database import engine
from src.models import post, comment


def test_handle_successfully(client, common_user, headers_with_authorized_common):
    # given
    with Session(engine) as session:
        post_ = post.Post(
            title="테스트 제목",
            user_id="heumsi",
            content="테스트 내용"
        )
        session.add(post_)
        comment_ = comment.Comment(
            id=1,
            post_id=post_.id,
            user_id=common_user.id,
            content="테스트 내용",
            post=post_,
            user=common_user
        )
        session.add(comment_)

        session.commit()
        session.refresh(comment_)
        session.refresh(common_user)
    time.sleep(1)  # wait for making difference between created_at, updated_at

    # when
    response = client.put(
        f"/comments/{comment_.id}",
        json={
            "content": "수정된 테스트 내용",
        },
        headers=headers_with_authorized_common,
    )

    # then
    assert response.status_code == status.HTTP_200_OK
    json_data = response.json()
    data = json_data.get("data")
    assert data == {
        "id": comment_.id,
        "post_id": comment_.post_id,
        "content": "수정된 테스트 내용",
        "user_id": common_user.id,
        "user_name": common_user.name,
        "created_at": data["created_at"],
        "updated_at": data["updated_at"],
    }
    assert data["updated_at"] > data["created_at"]
    with Session(engine) as session:
        statement = select(comment.Comment)
        results = session.exec(statement)
        comments = results.all()
        assert len(comments) == 1
        assert comments[0] == comment.Comment(
            id=comment_.id,
            post_id=comment_.post_id,
            content="수정된 테스트 내용",
            user_id=comments[0].user_id,
            created_at=comments[0].created_at,
            updated_at=comments[0].updated_at,
        )
        assert comments[0].updated_at > comments[0].created_at


def test_handle_unsuccessfully_with_no_authentication(client, common_user):
    # given
    with Session(engine) as session:
        post_ = post.Post(
            title="테스트 제목",
            user_id="heumsi",
            content="테스트 내용"
        )
        session.add(post_)
        comment_ = comment.Comment(
            id=1,
            post_id=post_.id,
            user_id=common_user.id,
            content="테스트 내용",
            post=post_,
            user=common_user
        )
        session.add(comment_)

        session.commit()
        session.refresh(comment_)
        session.refresh(common_user)

    # when
    response = client.put(
        f"/comments/{comment_.id}",
        json={
            "content": "수정된 테스트 내용",
        },
    )

    # then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_handle_unsuccessfully_with_no_authorization(client, common_user, headers_with_authorized_common_another):
    # given
    with Session(engine) as session:
        post_ = post.Post(
            title="테스트 제목",
            user_id="heumsi",
            content="테스트 내용"
        )
        session.add(post_)
        comment_ = comment.Comment(
            id=1,
            post_id=post_.id,
            user_id=common_user.id,
            content="테스트 내용",
            post=post_,
            user=common_user
        )
        session.add(comment_)

        session.commit()
        session.refresh(comment_)
        session.refresh(common_user)

    # when
    response = client.put(
        f"/comments/{comment_.id}",
        json={
            "content": "수정된 테스트 내용",
        },
        headers=headers_with_authorized_common_another
    )

    # then
    assert response.status_code == status.HTTP_403_FORBIDDEN
