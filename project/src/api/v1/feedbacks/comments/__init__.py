from fastapi import APIRouter, status

from src.api.v1.feedbacks.comments import (
    create_or_update_comment_feedback,
    delete_comment_feedback,
    get_comment_feedbacks,
)

router = APIRouter(prefix="/comments")

router.add_api_route(
    methods=["POST"],
    path="/{comment_id}/{like_or_dislike}",
    endpoint=create_or_update_comment_feedback.handle,
    summary="댓글에 대한 피드백을 추가하거나 기존에 존재하는 경우 업데이트 합니다.",
    responses={
        status.HTTP_200_OK: {
            "model": create_or_update_comment_feedback.UpdateCommentFeedbackResponse,
        },
        status.HTTP_201_CREATED: {
            "model": create_or_update_comment_feedback.CreateCommentFeedbackResponse,
        },
    },
)


router.add_api_route(
    methods=["GET"],
    path="/",
    endpoint=get_comment_feedbacks.handle,
    summary="댓글에 대한 피드백 목록을 조회합니다.",
    response_model=get_comment_feedbacks.GetCommentFeedbacksResponse,
)


router.add_api_route(
    methods=["DELETE"],
    path="/{comment_feedback_id}",
    endpoint=delete_comment_feedback.handle,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="댓글에 대한 피드백을 삭제합니다.",
)
