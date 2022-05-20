from fastapi import APIRouter, status, Depends

from src.api.auth.utils import GetAuthorizedUser
from src.api.users import read_users, get_me
from src.models.user import Role

router = APIRouter(prefix="/users", tags=["users"])

router.add_api_route(
    methods=["POST"],
    path="/",
    endpoint=read_users.handle,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(GetAuthorizedUser(allowed_roles=[Role.ADMIN]))],
    summary="유저 목록을 조회합니다.",
    response_model=read_users.ReadUsersResponse,
)

router.add_api_route(
    methods=["POST"],
    path="/me",
    endpoint=get_me.handle,
    status_code=status.HTTP_200_OK,
    summary="현재 로그인된 유저를 조회합니다.",
    response_model=get_me.GetMeResponse,
)
