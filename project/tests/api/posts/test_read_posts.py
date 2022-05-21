from fastapi import status
from sqlmodel import Session

from src.database import engine
from src.models import post


def test_handle_successfully(client):
    # given
    with Session(engine) as session:
        session.add(post.Post(
            id=1,
            title="테스트 제목",
            user_id="heumsi",
            content="테스트 내용"
        ))
        session.commit()

    # when
    response = client.get(
        "/posts/",
    )

    # then
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data == {
        "items": [
            {
                "id": 1,
                "title": "테스트 제목",
                "content": "테스트 내용",
                "created_at": data['items'][0]["created_at"],
                "updated_at": data['items'][0]["updated_at"],
                "user_id": data['items'][0]["user_id"],
            },
        ]
    }
