from fastapi import APIRouter, Depends, Response, status
import sys
from pathlib import Path


path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(path))

from app.exceptions import UserAlreadyExistsException, UserNotAuthenticatedException
from app.users.auth import authenticate_user, create_access_token, get_current_user
from app.users.models import Users
from app.users.password import HashPassword
from app.users.schemas import UserLoginSchema, UserRegisterSchema
from app.users.service import UserService


router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get('/me')
async def get_user_me(user: Users = Depends(get_current_user)):
    return user


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


@router.post('/login')
async def login_user(response: Response, user_data: UserLoginSchema) -> None:
    user = await authenticate_user(username=user_data.name, password=user_data.password)
    if user is None:
        raise UserNotAuthenticatedException
    access_token = create_access_token(data={'sub': user.id})
    response.set_cookie('myvkfeed_access_token', access_token, httponly=True)
    return {'access_token': access_token}



