from datetime import datetime, timedelta, timezone
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt


from app.config import settings
from app.exceptions import IncorrectCredentialsException
from app.users.models import Users
from app.users.password import HashPassword
from app.users.service import UserService


oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')


def create_access_token(data: dict) -> str:
    data_to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data_to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_schema)):  # -> UserResponseSchema:
    payload: dict = jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    username_from_token = payload.get('sub')
    # if username is None:
    #     raise InvalidUsernameException
    user = UserService.find_one_or_none(name=username_from_token)
    # if user is None:
    #     raise UserNotExistsException
    return user


async def authenticate_user(username: str, password: str) -> Users | None:
    existing_user = await UserService.find_one_or_none(name=username)
    if not HashPassword.verify_password(password, existing_user.hashed_password):
        raise IncorrectCredentialsException
    return existing_user

    





