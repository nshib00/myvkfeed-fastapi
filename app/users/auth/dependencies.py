import time
from fastapi import Depends, Request
import jwt

from app.config import settings
from app.exceptions import (
    ForbiddenException, InvalidTokenDataException, InvalidTokenException, TokenExpiredException, UserNotActiveException, UserNotExistsException,
    UserNotAuthenticatedException, InvalidTokenTypeException
) 
from app.users.auth.tokens.token_info import ACCESS_TOKEN_TYPE
from app.users.models import Users
from app.users.service import UserService


def get_token(request: Request) -> str:
    token = request.cookies.get('myvkfeed_access_token')
    if token is None:
        raise UserNotAuthenticatedException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload: dict = jwt.decode(token, key=settings.auth.SECRET_KEY, algorithms=[settings.auth.ALGORITHM])
    except jwt.PyJWTError:
        raise InvalidTokenException
    token_type: str = payload.get('type')
    if token_type != ACCESS_TOKEN_TYPE:
        raise InvalidTokenTypeException
    expire_date: str = payload.get('exp')
    if not expire_date or int(expire_date) < int(time.time()):
        raise TokenExpiredException
    user_id_from_token = payload.get('sub')
    if user_id_from_token is None:
        raise InvalidTokenDataException
    user = await UserService.find_one_or_none(id=int(user_id_from_token))
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