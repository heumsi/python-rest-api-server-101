from fastapi import APIRouter, status

from src.api.comments import create_comment, read_comment, read_comments, update_comment

router = APIRouter(prefix="/comments", tags=["comments"])

router.add_api_route(
    methods=["POST"],
    path="/",
    endpoint=create_comment.handle,
    status_code=status.HTTP_201_CREATED,
    summary="댓글을 추가합니다.",
    response_model=create_comment.CreateCommentResponse,
)

router.add_api_route(
    methods=["GET"],
    path="/{comment_id}",
    endpoint=read_comment.handle,
    status_code=status.HTTP_200_OK,
    summary="댓글을 조회합니다.",
    response_model=read_comment.ReadCommentResponse,
)

router.add_api_route(
    methods=["GET"],
    path="/",
    endpoint=read_comments.handle,
    status_code=status.HTTP_200_OK,
    summary="댓글 목록을 조회합니다.",
    response_model=read_comments.ReadCommentsResponse,
)

router.add_api_route(
    methods=["PUT"],
    path="/{comment_id}",
    endpoint=update_comment.handle,
    status_code=status.HTTP_200_OK,
    summary="댓글 전체를 수정합니다.",
    response_model=update_comment.UpdateCommentResponse,
)
