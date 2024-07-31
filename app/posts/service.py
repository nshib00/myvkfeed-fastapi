from sqlalchemy import select

from app.posts.models import Posts
from app.service.base import BaseService
from app.database import async_sessionmaker


class PostService(BaseService):
    model = Posts


    @classmethod
    async def find_non_existing_posts(cls, posts_list: list[Posts]) -> list[Posts]:
        non_existing_posts = []
        async with async_sessionmaker() as session:
            for post in posts_list:
                post_query = select(Posts).where(Posts.vk_id == post.vk_id)
                post_from_db = await session.execute(post_query)
                if post_from_db.one_or_none() is None:
                    non_existing_posts.append(post)
        return non_existing_posts
    

    @classmethod
    async def add_posts_list(cls, posts_list: list[Posts]) -> None:
        async with async_sessionmaker() as session: 
            for post in posts_list:
                await session.merge(post)
            await session.commit()