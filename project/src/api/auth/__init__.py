from fastapi import APIRouter, status

from src.api.auth import signup, signin

router = APIRouter(prefix="/auth", tags=["auth"])

router.add_api_route(
    methods=["POST"],
    path="/signup",
    endpoint=signup.handle,
    status_code=status.HTTP_201_CREATED,
    summary="새로운 유저로 가입합니다.",
)

router.add_api_route(
    methods=["POST"],
    path="/signin",
    endpoint=signin.handle,
    status_code=status.HTTP_200_OK,
    summary="로그인 합니다.",
)
