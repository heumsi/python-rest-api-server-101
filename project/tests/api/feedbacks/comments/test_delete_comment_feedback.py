from fastapi import status
from sqlmodel import Session, select

from src.database import engine
from src.models import comment, post
from src.models.feedbacks import comment_feedback


def test_handle_successfully(client, common_user, headers_with_authorized_common):
    # given
    with Session(engine) as session:
        post_ = post.Post(
            title="테스트 제목",
            user_id=common_user.id,
            content="테스트 내용",
        )
        comment_ = comment.Comment(
            post_id=post_.id,
            user_id=common_user.id,
            content="테스트 내용",
            post=post_,
            user=common_user,
        )
        feedback_ = comment_feedback.CommentFeedback(
            comment_id=comment_.id,
            user_id=common_user.id,
            like=True,
            comment=comment_,
            user=common_user,
        )
        session.add(post_)
        session.add(comment_)
        session.add(feedback_)
        session.commit()
        session.refresh(post_)
        session.refresh(comment_)
        session.refresh(feedback_)
        session.refresh(common_user)

    # when
    response = client.delete(
        f"/feedbacks/comments/{feedback_.id}",
        headers=headers_with_authorized_common,
    )

    # then
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with Session(engine) as session:
        statement = select(comment_feedback.CommentFeedback)
        results = session.exec(statement)
        comments = results.all()
        assert len(comments) == 0


def test_handle_unsuccessfully_with_not_found(client, headers_with_authorized_common):
    # when
    response = client.delete(
        "/feedbacks/comments/1", headers=headers_with_authorized_common
    )

    # then
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_handle_unsuccessfully_with_no_authentication(client):
    # when
    response = client.delete(
        "/feedbacks/comments/1",
    )

    # then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_handle_unsuccessfully_with_no_authorization(
    client, common_user, headers_with_authorized_common_another
):
    # given
    with Session(engine) as session:
        post_ = post.Post(
            title="테스트 제목",
            user_id=common_user.id,
            content="테스트 내용",
        )
        comment_ = comment.Comment(
            post_id=post_.id,
            user_id=common_user.id,
            content="테스트 내용",
            post=post_,
            user=common_user,
        )
        feedback_ = comment_feedback.CommentFeedback(
            comment_id=comment_.id,
            user_id=common_user.id,
            like=True,
            comment=comment_,
            user=common_user,
        )
        session.add(post_)
        session.add(comment_)
        session.add(feedback_)
        session.commit()
        session.refresh(post_)
        session.refresh(comment_)
        session.refresh(feedback_)
        session.refresh(common_user)

    # when
    response = client.delete(
        f"/feedbacks/comments/{feedback_.id}",
        headers=headers_with_authorized_common_another,
    )

    # then
    assert response.status_code == status.HTTP_403_FORBIDDEN
