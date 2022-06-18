from fastapi import FastAPI, status
from fastapi.responses import PlainTextResponse

from src.api.v1 import auth, comments, feedbacks, posts, users

app = FastAPI(
    title="Project REST API Docs",
    description="프로젝트 REST API 문서입니다.",
    version="v1",
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(feedbacks.router)


@app.get(
    "/",
    response_class=PlainTextResponse,
    status_code=status.HTTP_200_OK,
    summary="헬스체크용 엔드포인트 입니다.",
    description="API 서버가 잘 작동하는지 확인합니다.",
    response_description="API 서버가 잘 작동하고 있습니다.",
)
def healthcheck() -> str:
    return "I'm Alive!"
