from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.exceptions import UserAlreadyExistsException, UserNotAuthenticatedException
from app.users.auth.logic import authenticate_user, create_access_token
from app.users.auth.password import HashPassword
from app.users.schemas import UserRegisterSchema
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


@router.post('/login')
async def login_user(response: Response, user_data: OAuth2PasswordRequestForm = Depends()) -> None:
    user = await authenticate_user(username=user_data.username, password=user_data.password)
    if user is None:
        raise UserNotAuthenticatedException
    access_token = create_access_token(data={'sub': user.id})
    response.set_cookie('myvkfeed_access_token', access_token, httponly=True)
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/logout', status_code=status.HTTP_204_NO_CONTENT)
async def logout_user(response: Response) -> None:
    response.delete_cookie('myvkfeed_access_token', httponly=True)