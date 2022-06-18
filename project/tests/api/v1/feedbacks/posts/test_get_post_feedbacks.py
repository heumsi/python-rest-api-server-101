from fastapi import status
from sqlmodel import Session

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
        f"/v1/feedbacks/posts/",
    )

    # then
    assert response.status_code == status.HTTP_200_OK
    json_data = response.json()
    pagination = json_data.get("pagination")
    assert pagination == {"limit": 100, "offset": 0, "total": 4}
    data = json_data.get("data")
    assert data == [
        {
            "id": 1,
            "like": True,
            "createdAt": data[0]["createdAt"],
            "updatedAt": data[0]["updatedAt"],
            "user": {
                "id": common_user.id,
                "name": common_user.name,
            },
            "post": {
                "id": post_1.id,
            },
            "links": [
                {"href": f"{client.base_url}/v1/posts/{post_1.id}", "rel": "post"}
            ],
        },
        {
            "id": 2,
            "like": False,
            "createdAt": data[1]["createdAt"],
            "updatedAt": data[1]["updatedAt"],
            "user": {
                "id": common_another_user.id,
                "name": common_another_user.name,
            },
            "post": {
                "id": post_1.id,
            },
            "links": [
                {"href": f"{client.base_url}/v1/posts/{post_1.id}", "rel": "post"}
            ],
        },
        {
            "id": 3,
            "like": True,
            "createdAt": data[2]["createdAt"],
            "updatedAt": data[2]["updatedAt"],
            "user": {
                "id": common_user.id,
                "name": common_user.name,
            },
            "post": {
                "id": post_2.id,
            },
            "links": [
                {"href": f"{client.base_url}/v1/posts/{post_2.id}", "rel": "post"}
            ],
        },
        {
            "id": 4,
            "like": False,
            "createdAt": data[3]["createdAt"],
            "updatedAt": data[3]["updatedAt"],
            "user": {
                "id": common_another_user.id,
                "name": common_another_user.name,
            },
            "post": {
                "id": post_2.id,
            },
            "links": [
                {"href": f"{client.base_url}/v1/posts/{post_2.id}", "rel": "post"}
            ],
        },
    ]
    links = json_data.get("links")
    assert links == [{"href": f"{client.base_url}/v1/feedbacks/posts/", "rel": "self"}]


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
    response = client.get(f"/v1/feedbacks/posts/", params={"post_id": post_.id})

    # then
    assert response.status_code == status.HTTP_200_OK
    json_data = response.json()
    pagination = json_data.get("pagination")
    assert pagination == {"limit": 100, "offset": 0, "total": 2}
    data = json_data.get("data")
    assert [
        {
            "id": data[0]["id"],
            "like": True,
            "createdAt": data[0]["createdAt"],
            "updatedAt": data[0]["updatedAt"],
            "user": {
                "id": common_user.id,
                "name": common_user.name,
            },
            "post": {
                "id": post_.id,
            },
            "links": [
                {"href": f"{client.base_url}/v1/posts/{post_.id}", "rel": "post"}
            ],
        },
        {
            "id": data[1]["id"],
            "like": False,
            "createdAt": data[1]["createdAt"],
            "updatedAt": data[1]["updatedAt"],
            "user": {
                "id": common_another_user.id,
                "name": common_another_user.name,
            },
            "post": {
                "id": post_.id,
            },
            "links": [
                {"href": f"{client.base_url}/v1/posts/{post_.id}", "rel": "post"}
            ],
        },
    ]
    links = json_data.get("links")
    assert links == [
        {
            "href": f"{client.base_url}/v1/feedbacks/posts/?post_id={post_.id}",
            "rel": "self",
        }
    ]
