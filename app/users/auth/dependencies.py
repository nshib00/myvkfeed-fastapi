from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt

from app.config import settings
from app.exceptions import ForbiddenException, InvalidTokenException, UserNotActiveException, UserNotExistsException
from app.users.models import Users
from app.users.service import UserService


oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/login')


async def get_current_user(token: str = Depends(oauth2_schema)):
    try:
        payload: dict = jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_from_token = payload.get('sub')
        if user_id_from_token is None:
            raise InvalidTokenException
    except jwt.InvalidTokenError:
        raise InvalidTokenException
    user = await UserService.find_by_id(model_id=user_id_from_token)
    if user is None:
        raise UserNotExistsException
    return user


async def get_active_current_user(current_user: Users = Depends(get_current_user)) -> Users:
    if not current_user.is_active:
        raise UserNotActiveException
    return current_user


async def get_admin(current_user: Users = Depends(get_active_current_user)) -> Users:
    if not current_user.is_admin:
        raise ForbiddenException
    return current_user