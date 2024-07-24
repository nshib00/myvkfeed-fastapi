from fastapi import APIRouter
import sys
from pathlib import Path

from app.groups.service import GroupService
from vk.groups import load_user_groups


path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(path))


router = APIRouter(prefix='/groups', tags=['Группы ВК'])


@router.post('', status_code=201)
async def add_all_groups(user_id: int):
    groups = await load_user_groups(user_id=user_id)
    await GroupService.add_groups_list(groups)
        

@router.get('/load')
async def get_user_groups(user_id: int) -> list:
    groups = await load_user_groups(user_id=user_id)
    return groups


@router.get('')
async def get_saved_user_groups():
    return await GroupService.find_all()