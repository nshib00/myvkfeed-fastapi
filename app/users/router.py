from fastapi import APIRouter, Depends
import sys
from pathlib import Path


path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(path))

from app.users.auth.dependencies import get_active_current_user, get_admin
from app.users.models import Users
from app.users.schemas import ShortUserResponseSchema, UserResponseSchema
from app.users.service import UserService
from app.exceptions import UserNotExistsException


router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get('/me')
async def get_user_me(user: Users = Depends(get_active_current_user)) -> ShortUserResponseSchema:
    return user


@router.delete('/me/delete', status_code=204)
async def delete_user_me(user: Users = Depends(get_active_current_user)) -> None:
    await UserService.delete(Users.id == user.id)


@router.get('/list')
async def get_all_users(admin: Users = Depends(get_admin)) -> list[UserResponseSchema]:
    return await UserService.find_all()


@router.patch('/activate/{username}')
async def activate_user(username: str, admin: Users = Depends(get_admin)) -> None:
    activated_user_id = await UserService.update(username, is_active=True)
    if activated_user_id is None:
        raise UserNotExistsException
    return {'activated_user_id': activated_user_id}


@router.patch('/disable/{username}')
async def disable_user(username: str, admin: Users = Depends(get_admin)) -> None:
    disabled_user_id = await UserService.update(username, is_active=False)
    if disabled_user_id is None:
        raise UserNotExistsException
    return {'disabled_user_id': disabled_user_id}