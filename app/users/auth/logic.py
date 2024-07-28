from datetime import datetime, timedelta, timezone
import jwt


from app.config import settings
from app.exceptions import IncorrectCredentialsException
from app.users.models import Users
from app.users.auth.password import HashPassword
from app.users.service import UserService


def create_access_token(data: dict) -> str:
    data_to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data_to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(username: str, password: str) -> Users | None:
    existing_user = await UserService.find_one_or_none(name=username)
    if not HashPassword.verify_password(password, existing_user.hashed_password):
        raise IncorrectCredentialsException
    return existing_user

    





