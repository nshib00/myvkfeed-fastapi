from fastapi import APIRouter, Depends, Response, status

from app.exceptions import UserAlreadyExistsException, UserNotAuthenticatedException, IncorrectCredentialsException
from app.users.auth.dependencies import get_active_current_user
from app.users.auth.logic import authenticate_user, create_and_save_tokens
from app.users.auth.password_hash import HashPassword
from app.users.auth.tokens.service import RefreshTokenService
from app.users.auth.tokens.token_info import TokenInfo
from app.users.models import Users
from app.users.schemas import UserLoginSchema, UserRegisterSchema
from app.users.service import UserService


router = APIRouter(prefix='/auth', tags=['Аутентификация'])



@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegisterSchema) -> dict[str, int]:
    existing_user = await UserService.find_one_or_none(name=user_data.name)
    if existing_user is not None:
        raise UserAlreadyExistsException
    hashed_password = HashPassword.get_password_hash(user_data.password)
    registered_user_id = await UserService.add(
        name=user_data.name,
        vk_shortname=user_data.vk_shortname,
        hashed_password=hashed_password,
    )
    return {'registered_user_id': int(registered_user_id)}


@router.post('/refresh')
async def refresh_tokens(response: Response, user: Users = Depends(get_active_current_user)) -> TokenInfo:
    await RefreshTokenService.delete(token_user_id=user.id) # deleting old refresh tokens of current user
    tokens = await create_and_save_tokens(response, user)
    return tokens


@router.post('/login')
async def login_user(response: Response, user_data: UserLoginSchema) -> TokenInfo:
    user = await authenticate_user(username=user_data.name, password=user_data.password)
    tokens = await create_and_save_tokens(response, user)
    return tokens


@router.post('/logout', status_code=status.HTTP_204_NO_CONTENT)
async def logout_user(response: Response, user: Users = Depends(get_active_current_user)) -> None:
    response.delete_cookie('myvkfeed_access_token', httponly=True)
    await RefreshTokenService.delete(token_user_id=user.id)