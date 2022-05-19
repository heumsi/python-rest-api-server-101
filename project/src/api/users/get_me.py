from fastapi import Depends

from src.api.auth.utils import get_current_user
from src.models.user import UserBase, User


def handle(user: User = Depends(get_current_user)) -> UserBase:
    return user.to_user_base()
