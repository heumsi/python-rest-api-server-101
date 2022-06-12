from fastapi import status
from sqlmodel import Session

from src.database import engine
from src.models import comment, post


def test_handle_successfully(client, common_user, common_another_user):
    # given
    with Session(engine) as session:
        post_ = post.Post(
            title="테스트 제목",
            user_id=common_user.id,
            content="테스트 내용",
            user=common_user,
        )
        session.add(post_)
        session.add(comment.Comment(
            id=1,
            post_id=post_.id,
            user_id=common_user.id,
            content="테스트 내용 1",
            user=common_user,
            post=post_,
        ))
        session.add(comment.Comment(
            id=2,
            post_id=post_.id,
            user_id=common_another_user.id,
            content="테스트 내용 2",
            user=common_another_user,
            post=post_,
        ))
        session.commit()
        session.refresh(post_)
        session.refresh(common_user)
        session.refresh(common_another_user)

    # when
    response = client.get(
        "/comments/",
    )

    # then
    assert response.status_code == status.HTTP_200_OK
    json_data = response.json()
    data = json_data.get("data")
    assert data == [
        {
            "id": 1,
            "post_id": post_.id,
            "content": "테스트 내용 1",
            "created_at": data[0]["created_at"],
            "updated_at": data[0]["updated_at"],
            "user_id": common_user.id,
            "user_name": common_user.name,
            'links': [
                {
                    'href': f'{client.base_url}/comments/1',
                    'rel': 'self'
                },
                {
                    'href': f'{client.base_url}/posts/{post_.id}',
                    'rel': 'post'
                }
            ],
        },
        {
            "id": 2,
            "post_id": post_.id,
            "content": "테스트 내용 2",
            "created_at": data[0]["created_at"],
            "updated_at": data[0]["updated_at"],
            "user_id": common_another_user.id,
            "user_name": common_another_user.name,
            'links': [
                {
                    'href': f'{client.base_url}/comments/2',
                    'rel': 'self'
                },
                {
                    'href': f'{client.base_url}/posts/{post_.id}',
                    'rel': 'post'
                }
            ],
        },
    ]
    links = json_data.get("links")
    assert links == [
        {
            'href': f'{client.base_url}/comments/',
            'rel': 'self'
        }
    ]


def test_handle_successfully_with_params_including_post_id(client, common_user):
    # given
    with Session(engine) as session:
        post_1 = post.Post(
            title="테스트 제목 1",
            user_id=common_user.id,
            content="테스트 내용 1",
            user=common_user,
        )
        post_2 = post.Post(
            title="테스트 제목 2",
            user_id=common_user.id,
            content="테스트 내용 2",
            user=common_user,
        )
        session.add(post_1)
        session.add(post_2)

        comment_1 = comment.Comment(
            post_id=post_1.id,
            user_id=common_user.id,
            content="테스트 내용 1",
            user=common_user,
            post=post_1,
        )
        comment_2 = comment.Comment(
            post_id=post_2.id,
            user_id=common_user.id,
            content="테스트 내용 2",
            user=common_user,
            post=post_2,
        )
        session.add(comment_1)
        session.add(comment_2)

        session.commit()
        session.refresh(post_1)
        session.refresh(post_2)
        session.refresh(comment_1)
        session.refresh(comment_2)
        session.refresh(common_user)

    # when
    response = client.get(
        "/comments/",
        params={
            "post_id": post_1.id
        }
    )

    # then
    assert response.status_code == status.HTTP_200_OK
    json_data = response.json()
    data = json_data.get("data")
    assert data == [
        {
            "id": comment_1.id,
            "post_id": comment_1.post_id,
            "content": "테스트 내용 1",
            "created_at": data[0]["created_at"],
            "updated_at": data[0]["updated_at"],
            "user_id": common_user.id,
            "user_name": common_user.name,
            'links': [
                {
                    'href': f'{client.base_url}/comments/{comment_1.id}',
                    'rel': 'self'
                },
                {
                    'href': f'{client.base_url}/posts/{post_1.id}',
                    'rel': 'post'
                }
            ],
        },
    ]
    links = json_data.get("links")
    assert links == [
        {
            'href': f'{client.base_url}/comments/?post_id={post_1.id}',
            'rel': 'self'
        }
    ]