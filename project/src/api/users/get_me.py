from fastapi import Depends

from src.api.auth.utils import get_current_user
from src.model import User, UserBase


def handle(user: User = Depends(get_current_user)) -> UserBase:
    return user.to_user_base()
