from fastapi import APIRouter
import sys
from pathlib import Path

from app.groups.schemas import GroupSchema
from app.groups.service import GroupService
from vk.groups import load_user_groups


path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(path))


router = APIRouter(prefix='/groups', tags=['Группы ВК'])


@router.get('')
async def get_all_groups() -> list[GroupSchema]:
    return await GroupService.find_all()


@router.post('', status_code=201)
async def add_all_groups(user_id: int) -> None:
    groups = await load_user_groups(user_id=user_id)
    await GroupService.add_groups_list(groups)
        

@router.get('/load')
async def load_user_groups_from_vk(user_id: int) -> list[dict]:
    groups = await load_user_groups(user_id=user_id)
    return groups
