from fastapi import status
from sqlmodel import Session

from src.database import engine
from src.models import post, comment
from src.models.feedbacks import post_feedback


def test_handle_successfully(client, common_user):
    # given
    with Session(engine) as session:
        post_1 = post.Post(
            title="테스트 제목",
            user_id=common_user.id,
            user=common_user,
            content="테스트 내용"
        )
        feedback_1 = post_feedback.PostFeedback(
            post_id=post_1.id,
            user_id=common_user.id,
            like=True,
            post=post_1,
            user=common_user
        )
        comment_1 = comment.Comment(
            post_id=post_1.id,
            user_id=common_user.id,
            content="테스트 내용",
            post=post_1,
            user=common_user
        )
        post_2 = post.Post(
            title="테스트 제목",
            user_id=common_user.id,
            user=common_user,
            content="테스트 내용"
        )
        feedback_2 = post_feedback.PostFeedback(
            post_id=post_2.id,
            user_id=common_user.id,
            like=True,
            post=post_2,
            user=common_user
        )
        comment_2 = comment.Comment(
            post_id=post_2.id,
            user_id=common_user.id,
            content="테스트 내용",
            post=post_2,
            user=common_user
        )
        session.add(post_1)
        session.add(feedback_1)
        session.add(comment_1)
        session.add(post_2)
        session.add(feedback_2)
        session.add(comment_2)
        session.commit()
        session.refresh(post_1)
        session.refresh(post_2)
        session.refresh(common_user)

    # when
    response = client.get(
        "/posts/",
    )

    # then
    assert response.status_code == status.HTTP_200_OK
    json_data = response.json()
    data = json_data.get("data")
    assert data == [
        {
            "id": post_1.id,
            "title": "테스트 제목",
            "content": "테스트 내용",
            "created_at": data[0]["created_at"],
            "updated_at": data[0]["updated_at"],
            "user_id": common_user.id,
            "user_name": common_user.name,
            "num_likes": 1,
            "num_dislikes": 0,
            "num_comments": 1,
        },
        {
            "id": post_2.id,
            "title": "테스트 제목",
            "content": "테스트 내용",
            "created_at": data[0]["created_at"],
            "updated_at": data[0]["updated_at"],
            "user_id": common_user.id,
            "user_name": common_user.name,
            "num_likes": 1,
            "num_dislikes": 0,
            "num_comments": 1,
        },
    ]
