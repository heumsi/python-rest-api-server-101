from fastapi import APIRouter

from src.api.feedbacks import posts

router = APIRouter(prefix="/feedbacks", tags=["feedbacks"])

router.include_router(posts.router)