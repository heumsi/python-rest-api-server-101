from fastapi import HTTPException, status
from sqlmodel import Session

from src.api.auth.utils import pwd_context
from src.database import engine
from src.models.user import UserBase, UserSignup, User


def handle(user_signup: UserSignup) -> UserBase:
    with Session(engine) as session:
        user = session.get(User, user_signup.id)
        if user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exist")
        user_signup.password = pwd_context.hash(user_signup.password)
        new_user = User.from_orm(user_signup)
        session.add(new_user)
        session.commit()
        return new_user.to_user_base()
