from fastapi import status
from sqlmodel import Session

from src.database import engine
from src.models import comment, post


def test_handle_successfully(client, common_user):
    # given
    with Session(engine) as session:
        post_ = post.Post(
            title="테스트 제목",
            user_id=common_user.id,
            content="테스트 내용",
            user=common_user,
        )
        comment_ = comment.Comment(
            post_id=post_.id,
            user_id=common_user.id,
            content="테스트 내용",
            user=common_user,
            post=post_,
        )
        session.add(post_)
        session.add(comment_)
        session.commit()
        session.refresh(post_)
        session.refresh(comment_)
        session.refresh(common_user)

    # when
    response = client.get(
        f"/v1/comments/{comment_.id}",
    )

    # then
    assert response.status_code == status.HTTP_200_OK
    json_data = response.json()
    data = json_data.get("data")
    assert data == {
        "id": comment_.id,
        "content": "테스트 내용",
        "createdAt": data["createdAt"],
        "updatedAt": data["updatedAt"],
        "post": {
            "id": post_.id,
        },
        "user": {
            "id": common_user.id,
            "name": common_user.name,
        },
        "links": [
            {"href": f"{client.base_url}/v1/comments/1", "rel": "self"},
            {"href": f"{client.base_url}/v1/posts/1", "rel": "post"},
        ],
    }
    links = json_data.get("links")
    assert links == [
        {"href": f"{client.base_url}/v1/comments/{comment_.id}", "rel": "self"}
    ]


def test_handle_unsuccessfully_with_not_found(client):
    # when
    response = client.get(
        "/v1/comments/1",
    )

    # then
    assert response.status_code == status.HTTP_404_NOT_FOUND
