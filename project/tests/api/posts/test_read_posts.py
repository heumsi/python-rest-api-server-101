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

            "user": {
                "id": common_user.id,
                "name": common_user.name,
            },
            "num_of": {
                "likes": 1,
                "dislikes": 0,
                "comments": 1,
            },
            'links': [
                {
                    'href': f'{client.base_url}/posts/{post_1.id}', 
                    'rel': 'self'
                },
                {
                    'href': f'{client.base_url}/comments?post_id={post_1.id}', 
                    'rel': 'comments'
                },
                {
                    'href': f'{client.base_url}/feedbacks/posts?post_id={post_1.id}',
                    'rel': 'feedbacks'
                }
            ],
        },
        {
            "id": post_2.id,
            "title": "테스트 제목",
            "content": "테스트 내용",
            "created_at": data[0]["created_at"],
            "updated_at": data[0]["updated_at"],
            "user": {
                "id": common_user.id,
                "name": common_user.name,
            },
            "num_of": {
                "likes": 1,
                "dislikes": 0,
                "comments": 1,
            },
            'links': [
                {
                    'href': f'{client.base_url}/posts/{post_2.id}',
                    'rel': 'self'
                },
                {
                    'href': f'{client.base_url}/comments?post_id={post_2.id}',
                    'rel': 'comments'
                },
                {
                    'href': f'{client.base_url}/feedbacks/posts?post_id={post_2.id}',
                    'rel': 'feedbacks'
                }
            ],
            
        },
    ]
    links = json_data.get("links")
    assert links == [
        {
            'href': f'{client.base_url}/posts/',
            'rel': 'self'
        }
    ]