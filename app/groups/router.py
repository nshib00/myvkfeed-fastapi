from fastapi import APIRouter, Depends
import sys
from pathlib import Path

from app.exceptions import GroupNotExistsException
from app.groups.schemas import GroupSchema, GroupSchemaWithPosts
from app.groups.service import GroupService
from app.images.schemas import ImageResponseSchema
from app.posts.schemas import PostResponseSchemaWithImages
from app.users.auth.dependencies import get_active_current_user, get_admin
from app.users.models import Users
from vk.groups import load_user_groups
from vk.users import get_vk_user_id_by_shortname


path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(path))


router = APIRouter(prefix='/groups', tags=['Группы ВК'])


@router.get('')
async def get_all_groups(user: Users = Depends(get_active_current_user)) -> list[GroupSchema]:
    return await GroupService.find_all(user_id=user.id)


@router.get('/{group_id}')
async def get_group_by_id(group_id: int, user: Users = Depends(get_active_current_user)) -> GroupSchemaWithPosts:
    group = await GroupService.get_group_with_posts(group_id)
    if group is None:
        raise GroupNotExistsException
    return GroupSchemaWithPosts(
        id=group.id,
        title=group.title,
        source_id=group.source_id,
        is_hidden=group.is_hidden,
        user_id=group.user_id,
        posts=[
            PostResponseSchemaWithImages(
                id=post.id,
                pub_date=post.pub_date,
                text=post.text,
                images=[
                    ImageResponseSchema(url=img.url) for img in post.images
                ]
             ) for post in group.posts
        ],
    )


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


@router.delete('', status_code=204)
async def delete_all_groups(admin: Users = Depends(get_admin)) -> None:
    await GroupService.delete_all()