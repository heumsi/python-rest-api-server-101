from fastapi import status
from sqlmodel import Session, select

from src.database import engine
from src.models import post
from src.models.feedbacks import post_feedback


def test_handle_successfully_with_creating_post_feedback(
    client, common_user, headers_with_authorized_common
):
    # given
    with Session(engine) as session:
        post_ = post.Post(title="테스트 제목", user_id=common_user.id, content="테스트 내용")
        session.add(post_)
        session.commit()
        session.refresh(post_)

    # when
    response = client.post(
        f"/v1/feedbacks/posts/{post_.id}/like",
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
        "post": {
            "id": post_.id,
        },
    }

    with Session(engine) as session:
        statement = select(post_feedback.PostFeedback)
        results = session.exec(statement)
        post_feedbacks = results.all()
        assert len(post_feedbacks) == 1
        assert post_feedbacks[0] == post_feedback.PostFeedback(
            id=post_feedbacks[0].id,
            post_id=post_feedbacks[0].post_id,
            user_id=post_feedbacks[0].user_id,
            like=True,
            created_at=post_feedbacks[0].created_at,
            updated_at=post_feedbacks[0].updated_at,
        )


def test_handle_successfully_with_updating_post_feedback(
    client, common_user, headers_with_authorized_common
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
    response = client.post(
        f"/v1/feedbacks/posts/{post_.id}/dislike",
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
        "post": {
            "id": post_.id,
        },
    }

    with Session(engine) as session:
        statement = select(post_feedback.PostFeedback)
        results = session.exec(statement)
        post_feedbacks = results.all()
        assert len(post_feedbacks) == 1
        assert post_feedbacks[0] == post_feedback.PostFeedback(
            id=post_feedbacks[0].id,
            post_id=post_feedbacks[0].post_id,
            user_id=post_feedbacks[0].user_id,
            like=False,
            created_at=post_feedbacks[0].created_at,
            updated_at=post_feedbacks[0].updated_at,
        )


def test_handle_unsuccessfully_with_no_authentication(client):
    # when
    response = client.post(
        f"/v1/feedbacks/posts/1/like",
    )

    # then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
