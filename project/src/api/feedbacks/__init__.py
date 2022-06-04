from fastapi import APIRouter

from src.api.feedbacks import posts, comments

router = APIRouter(prefix="/feedbacks", tags=["feedbacks"])

router.include_router(posts.router)
router.include_router(comments.router)
