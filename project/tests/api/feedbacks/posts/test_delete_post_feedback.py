from sqlmodel import Session, select
from fastapi import status

from src.database import engine
from src.models import post
from src.models.feedbacks import post_feedback


def test_handle_successfully(
    client,
    common_user,
    headers_with_authorized_common
):
    # given
    with Session(engine) as session:
        post_ = post.Post(
            title="테스트 제목",
            user_id=common_user.id,
            content="테스트 내용",
        )
        feedback_ = post_feedback.PostFeedback(
            post_id=post_.id,
            user_id=common_user.id,
            like=True,
            post=post_,
            user=common_user,
        )
        session.add(post_)
        session.add(feedback_)
        session.commit()
        session.refresh(post_)
        session.refresh(feedback_)
        session.refresh(common_user)

    # when
    response = client.delete(
        f"/feedbacks/posts/{feedback_.id}",
        headers=headers_with_authorized_common,
    )

    # then
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with Session(engine) as session:
        statement = select(post_feedback.PostFeedback)
        results = session.exec(statement)
        comments = results.all()
        assert len(comments) == 0


def test_handle_unsuccessfully_with_not_found(client, headers_with_authorized_common):
    # when
    response = client.delete(
        "/feedbacks/posts/1",
        headers=headers_with_authorized_common
    )

    # then
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_handle_unsuccessfully_with_no_authentication(client):
    # when
    response = client.delete(
        "/feedbacks/posts/1",
    )

    # then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_handle_unsuccessfully_with_no_authorization(client, common_user, headers_with_authorized_common_another):
    # given
    with Session(engine) as session:
        post_ = post.Post(
            title="테스트 제목",
            user_id=common_user.id,
            content="테스트 내용",
        )
        feedback_ = post_feedback.PostFeedback(
            post_id=post_.id,
            user_id=common_user.id,
            like=True,
            post=post_,
            user=common_user,
        )
        session.add(post_)
        session.add(feedback_)
        session.commit()
        session.refresh(post_)
        session.refresh(feedback_)
        session.refresh(common_user)

    # when
    response = client.delete(
        f"/feedbacks/posts/{feedback_.id}",
        headers=headers_with_authorized_common_another,
    )

    # then
    assert response.status_code == status.HTTP_403_FORBIDDEN

