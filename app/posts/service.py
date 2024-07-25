from sqlalchemy import select
from sqlalchemy.exc import MultipleResultsFound

from app.exceptions import MultipleResultException
from app.posts.dto import PostDTO
from app.posts.models import Posts
from app.groups.models import Groups
from app.service.base import BaseService
from app.database import async_sessionmaker


class PostService(BaseService):
    model = Posts

    @classmethod
    async def add_posts_if_not_exist(cls, posts: list[Posts]) -> None:
        non_existing_posts = []
        async with async_sessionmaker() as session:
            for post in posts:
                post_query = select(Posts).where(Posts.vk_id == post.vk_id)
                post_from_db = await session.execute(post_query)
                if post_from_db.one_or_none() is None:
                    non_existing_posts.append(post)
            session.add_all(non_existing_posts)
            await session.commit()
    

    @classmethod
    async def add_posts_list(cls, posts: list) -> None:
        post_models = await PostDTO.raw_posts_to_models_list(posts)
        await cls.add_posts_if_not_exist(post_models)