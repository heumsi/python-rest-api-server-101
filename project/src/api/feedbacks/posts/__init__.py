from fastapi import APIRouter, status

from src.api.feedbacks.posts import create_or_update_post_feedback

router = APIRouter(prefix="/posts")

router.add_api_route(
    methods=["POST"],
    path="/{post_id}/{like_or_dislike}",
    endpoint=create_or_update_post_feedback.handle,
    summary="게시글에 대한 피드백을 추가하거나 기존에 존재하는 경우 업데이트 합니다.",
    responses={
        status.HTTP_200_OK: {
            "model": create_or_update_post_feedback.UpdatePostFeedbackResponse,
        },
        status.HTTP_201_CREATED: {
            "model": create_or_update_post_feedback.CreatePostFeedbackResponse,
        }
    }
)
