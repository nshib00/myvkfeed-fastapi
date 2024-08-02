from datetime import datetime, timedelta, timezone
from uuid import uuid4
from fastapi import Depends, Response
import jwt


from app.config import settings
from app.exceptions import IncorrectCredentialsException, InvalidTokenTypeException, UserNotExistsException
from app.users.auth.dependencies import get_active_current_user
from app.users.auth.tokens.service import RefreshTokenService
from app.users.auth.tokens.token_info import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, TokenInfo
from app.users.models import Users
from app.users.auth.password_hash import HashPassword
from app.users.service import UserService


def create_token(token_data: dict, token_type: str) -> str:
    data_to_encode = token_data.copy()
    if token_type == ACCESS_TOKEN_TYPE:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    elif token_type == REFRESH_TOKEN_TYPE:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.auth.REFRESH_TOKEN_EXPIRE_DAYS)
        data_to_encode |= {
            'jti': str(uuid4())
        }
    else:
        raise InvalidTokenTypeException
    data_to_encode |= {
        'exp': expire,
        'type': token_type
    }
    encoded_jwt = jwt.encode(data_to_encode, settings.auth.SECRET_KEY, algorithm=settings.auth.ALGORITHM)
    return encoded_jwt


def create_access_and_refresh_tokens(token_data: dict) -> TokenInfo:
    access_token = create_token(token_data=token_data, token_type=ACCESS_TOKEN_TYPE)
    refresh_token = create_token(token_data=token_data, token_type=REFRESH_TOKEN_TYPE)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token
    )


async def create_and_save_tokens(response: Response, user: Users = Depends(get_active_current_user)) -> TokenInfo:
    user_token_data = {'sub': user.id}
    tokens = create_access_and_refresh_tokens(token_data=user_token_data)
    response.set_cookie('myvkfeed_access_token', tokens.access_token, httponly=True)
    await RefreshTokenService.add(
        id=uuid4(),
        user_id=user.id,
        token=tokens.refresh_token,
    )
    return tokens
    

async def authenticate_user(username: str | None, password: str | None) -> Users | None:
    existing_user = await UserService.find_one_or_none(name=username)
    if existing_user is None:
        raise UserNotExistsException
    if not HashPassword.verify_password(password, existing_user.hashed_password):
        raise IncorrectCredentialsException
    return existing_user

    





