from fastapi import APIRouter, Depends
import sys
from pathlib import Path

from app.groups.schemas import GroupSchema
from app.groups.service import GroupService
from app.users.auth.dependencies import get_active_current_user
from app.users.models import Users
from vk.groups import load_user_groups
from vk.users import get_vk_user_id_by_shortname


path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(path))


router = APIRouter(prefix='/groups', tags=['Группы ВК'])


@router.get('')
async def get_all_groups(user: Users = Depends(get_active_current_user)) -> list[GroupSchema]:
    return await GroupService.find_all(user_id=user.id)


@router.post('', status_code=201)
async def add_all_groups(user: Users = Depends(get_active_current_user)) -> None:
    vk_user_id: int = await get_vk_user_id_by_shortname(vk_shortname=user.vk_shortname)
    groups = await load_user_groups(user_id=vk_user_id)
    await GroupService.add_groups_list(groups, user_id=user.id)
        

@router.get('/load')
async def load_user_groups_from_vk(user: Users = Depends(get_active_current_user)) -> list[dict]:
    vk_user_id: int = await get_vk_user_id_by_shortname(vk_shortname=user.vk_shortname)
    groups = await load_user_groups(user_id=vk_user_id)
    return groups
