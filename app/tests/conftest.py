import asyncio
from httpx import AsyncClient
import pytest
from sqlalchemy import insert
from datetime import datetime

from app.database import Base, engine, async_sessionmaker
from app.config import settings
from app.tests.data.faker import dump_fake_data, load_fake_data
from app.main import app as fastapi_app

from app.users.models import Users
from app.groups.models import Groups
from app.posts.models import Posts
from app.images.models import PostImages, GroupImages


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    assert settings.mode == 'test'

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    dump_fake_data()

    fake_users = load_fake_data('users')
    fake_groups = load_fake_data('groups')
    fake_posts = load_fake_data('posts')

    for user in fake_users:
        user['date_joined'] = datetime.strptime(user['date_joined'], '%Y-%m-%d %H:%M:%S')
    for post in fake_posts:
        post['pub_date'] = datetime.strptime(post['pub_date'], '%Y-%m-%d %H:%M:%S') 


    async with async_sessionmaker() as session:
        users_insert = insert(Users).values(fake_users)
        posts_insert = insert(Posts).values(fake_posts)
        groups_insert = insert(Groups).values(fake_groups)
        for query in (users_insert, posts_insert, groups_insert):
            await session.execute(query)
        await session.commit()


@pytest.fixture(scope='function')
async def client():
    async with AsyncClient(app=fastapi_app, base_url='http://test') as cli:
        yield cli 


