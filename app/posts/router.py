from fastapi import APIRouter, status
import sys
from pathlib import Path


path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(path))
from app.posts.schemas import PostSchema
from app.posts.service import PostService
from vk.posts import load_user_feed


router = APIRouter(prefix='/posts', tags=['Посты'])


@router.get('')
async def get_all_posts() -> list[PostSchema]:
    return await PostService.find_all()


@router.post('', status_code=status.HTTP_201_CREATED)
async def add_all_posts() -> None:
    posts = await load_user_posts_from_vk()
    await PostService.add_posts_list(posts)
    # TODO если добавляется хотя бы 1 пост/группа, оставить код 201, если ничего не добавляется - изменить на 200
    

@router.get('/load')
async def load_user_posts_from_vk() -> list:
    posts = await load_user_feed()
    return posts

