from fastapi import APIRouter, status

from src.api.auth import signup

router = APIRouter(prefix="/auth", tags=["auth"])

router.add_api_route(
    methods=["POST"],
    path="/signup",
    endpoint=signup.handle,
    status_code=status.HTTP_201_CREATED
)

