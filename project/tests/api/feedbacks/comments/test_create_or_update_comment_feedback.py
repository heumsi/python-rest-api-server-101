from sqlmodel import Session, select
from fastapi import status

from src.database import engine
from src.models import post, comment
from src.models.feedbacks import comment_feedback


def test_handle_successfully_with_creating_comment_feedback(
    client, common_user, headers_with_authorized_common
):
    # given
    with Session(engine) as session:
        post_ = post.Post(title="테스트 제목", user_id=common_user.id, content="테스트 내용")
        comment_ = comment.Comment(
            post_id=post_.id,
            user_id=common_user.id,
            content="테스트 내용",
            post=post_,
            user=common_user,
        )
        session.add(post_)
        session.add(comment_)
        session.commit()
        session.refresh(post_)
        session.refresh(comment_)
        session.refresh(common_user)

    # when
    response = client.post(
        f"/feedbacks/comments/{comment_.id}/like",
        headers=headers_with_authorized_common,
    )

    # then
    assert response.status_code == status.HTTP_201_CREATED
    json_data = response.json()
    data = json_data.get("data")
    assert data == {
        "id": data["id"],
        "like": True,
        "createdAt": data["createdAt"],
        "updatedAt": data["updatedAt"],
        "user": {
            "id": common_user.id,
        },
        "comment": {
            "id": comment_.id,
        },
    }

    with Session(engine) as session:
        statement = select(comment_feedback.CommentFeedback)
        results = session.exec(statement)
        comment_feedbacks = results.all()
        assert len(comment_feedbacks) == 1
        assert comment_feedbacks[0] == comment_feedback.CommentFeedback(
            id=comment_feedbacks[0].id,
            comment_id=comment_feedbacks[0].comment_id,
            user_id=comment_feedbacks[0].user_id,
            like=True,
            created_at=comment_feedbacks[0].created_at,
            updated_at=comment_feedbacks[0].updated_at,
        )


def test_handle_successfully_with_updating_comment_feedback(
    client, common_user, headers_with_authorized_common
):
    # given
    with Session(engine) as session:
        post_ = post.Post(title="테스트 제목", user_id=common_user.id, content="테스트 내용")
        comment_ = comment.Comment(
            post_id=post_.id,
            user_id=common_user.id,
            content="테스트 내용",
            post=post_,
            user=common_user,
        )
        comment_feedback_ = comment_feedback.CommentFeedback(
            comment_id=comment_.id,
            user_id=common_user.id,
            like=True,
            comment=comment_,
            user=common_user,
        )
        session.add(post_)
        session.add(comment_)
        session.add(comment_feedback_)
        session.commit()
        session.refresh(post_)
        session.refresh(comment_)
        session.refresh(comment_feedback_)
        session.refresh(common_user)

    # when
    response = client.post(
        f"/feedbacks/comments/{comment_.id}/dislike",
        headers=headers_with_authorized_common,
    )

    # then
    assert response.status_code == status.HTTP_200_OK
    json_data = response.json()
    data = json_data.get("data")
    assert data == {
        "id": data["id"],
        "like": False,
        "createdAt": data["createdAt"],
        "updatedAt": data["updatedAt"],
        "user": {
            "id": common_user.id,
        },
        "comment": {
            "id": comment_.id,
        },
    }
    with Session(engine) as session:
        statement = select(comment_feedback.CommentFeedback)
        results = session.exec(statement)
        comment_feedbacks = results.all()
        assert len(comment_feedbacks) == 1
        assert comment_feedbacks[0] == comment_feedback.CommentFeedback(
            id=comment_feedbacks[0].id,
            comment_id=comment_feedbacks[0].comment_id,
            user_id=comment_feedbacks[0].user_id,
            like=False,
            created_at=comment_feedbacks[0].created_at,
            updated_at=comment_feedbacks[0].updated_at,
        )


def test_handle_unsuccessfully_with_not_found(client, headers_with_authorized_common):
    # when
    response = client.post(
        f"/feedbacks/comments/1/like",
        headers=headers_with_authorized_common,
    )

    # then
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_handle_unsuccessfully_with_no_authentication(client):
    # when
    response = client.post(
        f"/feedbacks/comments/1/like",
    )

    # then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
