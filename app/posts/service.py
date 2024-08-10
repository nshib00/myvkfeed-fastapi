from sqlalchemy import select

from app.groups.models import Groups
from app.images.models import PostImages
from app.posts.models import Posts
from app.service.base import BaseService
from app.database import async_sessionmaker
from app.posts.schemas import PostSchema


class PostService(BaseService):
    model = Posts


    @classmethod
    async def find_non_existing_posts(cls, posts_list: list[PostSchema]) -> list[PostSchema]:
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

    
    @classmethod
    async def get_post_with_images(cls, post_id: int) -> Posts | None:
        async with async_sessionmaker() as session:
            group_query = select(Posts).where(Posts.id == post_id)
            group_result = await session.execute(group_query)
            return group_result.scalar()
        
    @classmethod
    async def get_posts_with_group_and_images(cls) -> list[Posts]:
        async with async_sessionmaker() as session:
            group_query = select(Posts).join(
                PostImages, PostImages.post_id == Posts.id
            ).join(
                Groups, Groups.id == Posts.group_id
            ).distinct()
            group_result = await session.execute(group_query)
            return group_result.scalars().all()
