from fastapi import APIRouter

from src.api.feedbacks import comments, posts

router = APIRouter(prefix="/feedbacks", tags=["feedbacks"])

router.include_router(posts.router)
router.include_router(comments.router)
