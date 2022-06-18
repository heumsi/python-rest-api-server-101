from fastapi import status
from sqlmodel import Session

from src.database import engine
from src.models import comment, post
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
            user=common_user,
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
            user=common_user,
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
        f"/v1/feedbacks/comments/",
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
            "comment": {
                "id": comment_1.id,
            },
            "links": [
                {
                    "href": f"{client.base_url}/v1/comments/{comment_1.id}",
                    "rel": "comment",
                }
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
            "comment": {
                "id": comment_1.id,
            },
            "links": [
                {
                    "href": f"{client.base_url}/v1/comments/{comment_1.id}",
                    "rel": "comment",
                },
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
            "comment": {
                "id": comment_2.id,
            },
            "links": [
                {
                    "href": f"{client.base_url}/v1/comments/{comment_2.id}",
                    "rel": "comment",
                },
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
            "comment": {
                "id": comment_2.id,
            },
            "links": [
                {
                    "href": f"{client.base_url}/v1/comments/{comment_2.id}",
                    "rel": "comment",
                },
            ],
        },
    ]
    links = json_data.get("links")
    assert links == [
        {"href": f"{client.base_url}/v1/feedbacks/comments/", "rel": "self"},
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
            user=common_user,
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
            user=common_user,
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
        f"/v1/feedbacks/comments/", params={"comment_id": comment_1.id}
    )

    # then
    assert response.status_code == status.HTTP_200_OK
    json_data = response.json()
    pagination = json_data.get("pagination")
    assert pagination == {"limit": 100, "offset": 0, "total": 2}
    data = json_data.get("data")
    assert data == [
        {
            "id": data[0]["id"],
            "like": True,
            "createdAt": data[0]["createdAt"],
            "updatedAt": data[0]["updatedAt"],
            "user": {
                "id": common_user.id,
                "name": common_user.name,
            },
            "comment": {
                "id": comment_1.id,
            },
            "links": [
                {
                    "href": f"{client.base_url}/v1/comments/{comment_1.id}",
                    "rel": "comment",
                },
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
            "comment": {
                "id": comment_1.id,
            },
            "links": [
                {
                    "href": f"{client.base_url}/v1/comments/{comment_1.id}",
                    "rel": "comment",
                },
            ],
        },
    ]
    links = json_data.get("links")
    assert links == [
        {
            "href": f"{client.base_url}/v1/feedbacks/comments/?comment_id={comment_1.id}",
            "rel": "self",
        },
    ]
