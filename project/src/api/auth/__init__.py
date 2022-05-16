from fastapi import APIRouter, status

from src.api.auth import signup, signin

router = APIRouter(prefix="/auth", tags=["auth"])

router.add_api_route(
    methods=["POST"],
    path="/signup",
    endpoint=signup.handle,
    status_code=status.HTTP_201_CREATED
)

router.add_api_route(
    methods=["POST"],
    path="/signin",
    endpoint=signin.handle,
    status_code=status.HTTP_200_OK
)
