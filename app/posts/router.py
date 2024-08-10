from fastapi import APIRouter, Depends, Response, status
import sys
from pathlib import Path

from app.groups.service import GroupService
from app.users.auth.dependencies import get_active_current_user, get_admin
from app.users.models import Users


path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(path))

from app.posts.dto import PostDTO
from app.exceptions import NoGroupsException, PostNotExistsException
from app.posts.schemas import PostSchema, PostResponseSchemaWithImages, PostResponseRenderSchema
from app.posts.service import PostService

from vk.posts import load_user_feed


router = APIRouter(prefix='/posts', tags=['Посты'])


@router.get('/all')
async def get_all_posts(user: Users = Depends(get_active_current_user)) -> list[PostSchema]:
    return await PostService.find_all()


@router.get('/all_with_related')
async def get_all_posts_with_related_data(user: Users = Depends(get_active_current_user)) -> list[PostResponseRenderSchema]:
    post_models = await PostService.get_posts_with_group_and_images()
    return PostDTO.many_models_to_schemas(post_models, with_group_title=True)


@router.get('/{post_id}')
async def get_post_by_id(post_id: int, user: Users = Depends(get_active_current_user)) -> PostResponseRenderSchema:
    post = await PostService.get_post_with_images(post_id=post_id)
    if post is None:
        raise PostNotExistsException
    return PostDTO.one_model_to_schema(post_model=post, with_group_title=True)


@router.post('', status_code=status.HTTP_201_CREATED)
async def add_all_posts(response: Response, user: Users = Depends(get_active_current_user)) -> dict[str, int]:
    if not await GroupService.find_all():
        raise NoGroupsException
    posts = await load_user_posts_from_vk()
    post_models = await PostDTO.raw_posts_to_models_list(posts)
    non_existing_posts = await PostService.find_non_existing_posts(posts_list=post_models)
    if non_existing_posts:
        await PostService.add_posts_list(non_existing_posts)
    else:
        response.status_code = status.HTTP_200_OK
    return {'added_posts_count': len(non_existing_posts)}
    
    
@router.get('/load')
async def load_user_posts_from_vk(user: Users = Depends(get_active_current_user)) -> list[dict]:
    posts = await load_user_feed()
    return posts


@router.delete('', status_code=204)
async def delete_all_posts(admin: Users = Depends(get_admin)) -> None:
    await PostService.delete_all()
