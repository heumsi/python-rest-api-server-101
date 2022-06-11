from sqlmodel import Session
from fastapi import status

from src.database import engine
from src.models import post, comment
from src.models.feedbacks import comment_feedback


def test_handle_successfully(
    client,
    common_user,
    common_another_user,
    headers_with_authorized_common,
    headers_with_authorized_common_another,
):
    # given
    with Session(engine) as session:
        post_1 = post.Post(
            title="테스트 제목",
            user_id=common_user.id,
            content="테스트 내용",
        )
        comment_1 = comment.Comment(
            post_id=post_1.id,
            user_id=common_user.id,
            content="테스트 내용",
            post=post_1,
            user=common_user
        )
        comment_feedback_1_1 = comment_feedback.CommentFeedback(
            comment_id=comment_1.id,
            user_id=common_user.id,
            like=True,
            comment=comment_1,
            user=common_user,
        )
        comment_feedback_1_2 = comment_feedback.CommentFeedback(
            comment_id=comment_1.id,
            user_id=common_another_user.id,
            like=False,
            comment=comment_1,
            user=common_another_user,
        )
        post_2 = post.Post(
            title="테스트 제목",
            user_id=common_user.id,
            content="테스트 내용",
        )
        comment_2 = comment.Comment(
            post_id=post_2.id,
            user_id=common_user.id,
            content="테스트 내용",
            post=post_2,
            user=common_user
        )
        comment_feedback_2_1 = comment_feedback.CommentFeedback(
            comment_id=comment_2.id,
            user_id=common_user.id,
            like=True,
            comment=comment_2,
            user=common_user,
        )
        comment_feedback_2_2 = comment_feedback.CommentFeedback(
            comment_id=comment_2.id,
            user_id=common_another_user.id,
            like=False,
            comment=comment_2,
            user=common_another_user,
        )

        session.add(post_1)
        session.add(comment_1)
        session.add(comment_feedback_1_1)
        session.add(comment_feedback_1_2)
        session.add(post_2)
        session.add(comment_2)
        session.add(comment_feedback_2_1)
        session.add(comment_feedback_2_2)
        session.commit()
        session.refresh(post_1)
        session.refresh(comment_1)
        session.refresh(comment_feedback_1_1)
        session.refresh(comment_feedback_1_2)
        session.refresh(post_2)
        session.refresh(comment_2)
        session.refresh(comment_feedback_2_1)
        session.refresh(comment_feedback_2_2)
        session.refresh(common_user)
        session.refresh(common_another_user)


    # when
    response = client.get(
        f"/feedbacks/comments/",
    )

    # then
    assert response.status_code == status.HTTP_200_OK
    json_data = response.json()
    data = json_data.get("data")
    assert data == [
        {
            'id': 1,
            'comment_id': comment_1.id,
            'user_id': common_user.id,
            'user_name': common_user.name,
            'like': True,
            'created_at': data[0]['created_at'],
            'updated_at': data[0]['updated_at'],
        }, {
            'id': 2,
            'comment_id': comment_1.id,
            'user_id': common_another_user.id,
            'user_name': common_another_user.name,
            'like': False,
            'created_at': data[1]['created_at'],
            'updated_at': data[1]['updated_at'],
        }, {
            'id': 3,
            'comment_id': comment_2.id,
            'user_id': common_user.id,
            'user_name': common_user.name,
            'like': True,
            'created_at': data[2]['created_at'],
            'updated_at': data[2]['updated_at'],
        }, {
            'id': 4,
            'comment_id': comment_2.id,
            'user_id': common_another_user.id,
            'user_name': common_another_user.name,
            'like': False,
            'created_at': data[3]['created_at'],
            'updated_at': data[3]['updated_at'],
        }
    ]


def test_handle_successfully_with_specific_post_id(
        client,
        common_user,
        common_another_user,
        headers_with_authorized_common,
        headers_with_authorized_common_another,
):
    # given
    with Session(engine) as session:
        post_1 = post.Post(
            title="테스트 제목",
            user_id=common_user.id,
            content="테스트 내용",
        )
        comment_1 = comment.Comment(
            post_id=post_1.id,
            user_id=common_user.id,
            content="테스트 내용",
            post=post_1,
            user=common_user
        )
        comment_feedback_1_1 = comment_feedback.CommentFeedback(
            comment_id=comment_1.id,
            user_id=common_user.id,
            like=True,
            comment=comment_1,
            user=common_user,
        )
        comment_feedback_1_2 = comment_feedback.CommentFeedback(
            comment_id=comment_1.id,
            user_id=common_another_user.id,
            like=False,
            comment=comment_1,
            user=common_another_user,
        )
        post_2 = post.Post(
            title="테스트 제목",
            user_id=common_user.id,
            content="테스트 내용",
        )
        comment_2 = comment.Comment(
            post_id=post_2.id,
            user_id=common_user.id,
            content="테스트 내용",
            post=post_2,
            user=common_user
        )
        comment_feedback_2_1 = comment_feedback.CommentFeedback(
            comment_id=comment_2.id,
            user_id=common_user.id,
            like=True,
            comment=comment_2,
            user=common_user,
        )
        comment_feedback_2_2 = comment_feedback.CommentFeedback(
            comment_id=comment_2.id,
            user_id=common_another_user.id,
            like=False,
            comment=comment_2,
            user=common_another_user,
        )

        session.add(post_1)
        session.add(comment_1)
        session.add(comment_feedback_1_1)
        session.add(comment_feedback_1_2)
        session.add(post_2)
        session.add(comment_2)
        session.add(comment_feedback_2_1)
        session.add(comment_feedback_2_2)
        session.commit()
        session.refresh(post_1)
        session.refresh(comment_1)
        session.refresh(comment_feedback_1_1)
        session.refresh(comment_feedback_1_2)
        session.refresh(post_2)
        session.refresh(comment_2)
        session.refresh(comment_feedback_2_1)
        session.refresh(comment_feedback_2_2)
        session.refresh(common_user)
        session.refresh(common_another_user)

    # when
    response = client.get(
        f"/feedbacks/comments/",
        params={
            "comment_id": comment_1.id
        }
    )

    # then
    assert response.status_code == status.HTTP_200_OK
    json_data = response.json()
    data = json_data.get("data")
    assert data == [
        {
            "id": data[0]["id"],
            "user_id": common_user.id,
            "user_name": common_user.name,
            "comment_id": comment_1.id,
            "like": True,
            "created_at": data[0]["created_at"],
            "updated_at": data[0]["updated_at"],
        },
        {
            "id": data[1]["id"],
            "user_id": common_another_user.id,
            "user_name": common_another_user.name,
            "comment_id": comment_1.id,
            "like": False,
            "created_at": data[1]["created_at"],
            "updated_at": data[1]["updated_at"],
        }
    ]

