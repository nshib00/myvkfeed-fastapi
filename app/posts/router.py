from fastapi import APIRouter
import sys
from pathlib import Path


path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(path))
# from vk_old.main_logic import MyVkFeedLogic
from vk.json_handler import load_posts_from_json, save_posts_to_json
from vk.posts import load_user_feed


router = APIRouter(prefix='/posts', tags=['Посты'])


# @router.post('')
# async def add_new_posts():
#     pass


@router.get('')
async def get_all_posts():
    posts = load_posts_from_json()
    return posts


@router.get('/load')
async def load_posts():
    posts = await load_user_feed()
    save_posts_to_json(posts)
    return posts

