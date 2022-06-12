from sqlmodel import Session
from fastapi import status

from src.database import engine
from src.models import post
from src.models.feedbacks import post_feedback


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
        feedback_1_1 = post_feedback.PostFeedback(
            post_id=post_1.id,
            user_id=common_user.id,
            like=True,
            post=post_1,
            user=common_user,
        )
        feedback_1_2 = post_feedback.PostFeedback(
            post_id=post_1.id,
            user_id=common_another_user.id,
            like=False,
            post=post_1,
            user=common_another_user,
        )
        session.add(post_1)
        session.add(feedback_1_1)
        session.add(feedback_1_2)
        session.commit()

        post_2 = post.Post(
            title="테스트 제목 2",
            user_id=common_user.id,
            content="테스트 내용 2",
        )
        feedback_2_1 = post_feedback.PostFeedback(
            post_id=post_2.id,
            user_id=common_user.id,
            like=True,
            post=post_2,
            user=common_user,
        )
        feedback_2_2 = post_feedback.PostFeedback(
            post_id=post_2.id,
            user_id=common_another_user.id,
            like=False,
            post=post_2,
            user=common_another_user,
        )
        session.add(post_2)
        session.add(feedback_2_1)
        session.add(feedback_2_2)
        session.commit()

        session.refresh(post_1)
        session.refresh(feedback_1_1)
        session.refresh(feedback_1_2)
        session.refresh(post_2)
        session.refresh(feedback_2_1)
        session.refresh(feedback_2_2)
        session.refresh(common_user)
        session.refresh(common_another_user)

    # when
    response = client.get(
        f"/feedbacks/posts/",
    )

    # then
    assert response.status_code == status.HTTP_200_OK
    json_data = response.json()
    data = json_data.get("data")
    assert data == [
        {
            'id': 1,
            'post_id': post_1.id,
            'user_id': common_user.id,
            'user_name': common_user.name,
            'like': True,
            'created_at': data[0]['created_at'],
            'updated_at': data[0]['updated_at'],
            'links': [
                {
                    'href': f'{client.base_url}/posts/{post_1.id}',
                    'rel': 'post'
                }
            ],
        }, {
            'id': 2,
            'post_id': post_1.id,
            'user_id': common_another_user.id,
            'user_name': common_another_user.name,
            'like': False,
            'created_at': data[1]['created_at'],
            'updated_at': data[1]['updated_at'],
            'links': [
                {
                    'href': f'{client.base_url}/posts/{post_1.id}',
                    'rel': 'post'
                }
            ],
        }, {
            'id': 3,
            'post_id': post_2.id,
            'user_id': common_user.id,
            'user_name': common_user.name,
            'like': True,
            'created_at': data[2]['created_at'],
            'updated_at': data[2]['updated_at'],
            'links': [
                {
                    'href': f'{client.base_url}/posts/{post_2.id}',
                    'rel': 'post'
                }
            ],
        }, {
            'id': 4,
            'post_id': post_2.id,
            'user_id': common_another_user.id,
            'user_name': common_another_user.name,
            'like': False,
            'created_at': data[3]['created_at'],
            'updated_at': data[3]['updated_at'],
            'links': [
                {
                    'href': f'{client.base_url}/posts/{post_2.id}',
                    'rel': 'post'
                }
            ],
        }
    ]
    links = json_data.get("links")
    assert links == [
        {
            'href': f'{client.base_url}/feedbacks/posts/',
            'rel': 'self'
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
        feedback_by_another = post_feedback.PostFeedback(
            post_id=post_.id,
            user_id=common_another_user.id,
            like=False,
            post=post_,
            user=common_another_user,
        )
        session.add(post_)
        session.add(feedback_)
        session.add(feedback_by_another)
        session.commit()
        session.refresh(post_)
        session.refresh(feedback_)
        session.refresh(common_user)
        session.refresh(common_another_user)

    # when
    response = client.get(
        f"/feedbacks/posts/",
        params={
            "post_id": post_.id
        }
    )

    # then
    assert response.status_code == status.HTTP_200_OK
    json_data = response.json()
    data = json_data.get("data")
    assert [
        {
            "id": data[0]["id"],
            "user_id": common_user.id,
            "user_name": common_user.name,
            "post_id": post_.id,
            "like": True,
            "created_at": data[0]["created_at"],
            "updated_at": data[0]["updated_at"],
            'links': [
                {
                    'href': f'{client.base_url}/posts/{post_.id}',
                    'rel': 'post'
                }
            ],
        },
        {
            "id": data[1]["id"],
            "user_id": common_another_user.id,
            "user_name": common_another_user.name,
            "post_id": post_.id,
            "like": False,
            "created_at": data[1]["created_at"],
            "updated_at": data[1]["updated_at"],
            'links': [
                {
                    'href': f'{client.base_url}/posts/{post_.id}',
                    'rel': 'post'
                }
            ],
        }
    ]
    links = json_data.get("links")
    assert links == [
        {
            'href': f'{client.base_url}/feedbacks/posts/?post_id={post_.id}',
            'rel': 'self'
        }
    ]
