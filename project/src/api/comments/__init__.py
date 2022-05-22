from fastapi import APIRouter, status

from src.api.comments import create_comment

router = APIRouter(prefix="/comments", tags=["comments"])

router.add_api_route(
    methods=["POST"],
    path="/",
    endpoint=create_comment.handle,
    status_code=status.HTTP_201_CREATED,
    summary="댓글을 추가합니다.",
    response_model=create_comment.CreateCommentResponse,
)
