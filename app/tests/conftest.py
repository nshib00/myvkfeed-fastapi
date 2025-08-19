import asyncio
from faker import Faker
from httpx import ASGITransport, AsyncClient
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


@pytest.fixture(scope='session')
async def faker():
    return Faker()


@pytest.fixture(scope='session')
async def test_user(faker):
    async with async_sessionmaker() as session:
        new_user = Users(
            name='test_user',
            vk_shortname='test',
            hashed_password=faker.sha256(),
            date_joined=faker.date_time(),
            is_active=True,
            is_admin=False,
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
    return new_user


@pytest.fixture(scope='session')
async def authenticated_client(test_user):
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app),
        base_url='http://test',
    ) as ac:
        await ac.post(
            url='/auth/login',
            json={
                'name': test_user.name,
                'password': test_user.password,
            }
        )  
        assert ac.cookies.get('booking_access_token') is not None
        yield ac 


@pytest.fixture(scope='session')
async def groups(test_user):
    groups_data = [
        Groups(source_id=1001, title="Group 1", user_id=test_user.id),
        Groups(source_id=1002, title="Group 2", user_id=test_user.id),
        Groups(source_id=1003, title="Hidden group 1", user_id=test_user.id, is_hidden=True),
        Groups(source_id=1004, title="Hidden group 2", user_id=test_user.id, is_hidden=True),
    ]
    async with async_sessionmaker() as session:
        session.add_all(groups_data)
        await session.commit()
        for g in groups_data:
            await session.refresh(g)
    return groups_data


@pytest.fixture(scope='session')
async def group_images(groups):
    async with async_sessionmaker() as session:
        for group in groups:
            group_image = GroupImages(
                url=f"https://example.com/group-image-{group.id}.jpg",
                group_id=group.id,
            )
            session.add(group_image)
            await session.commit()
            await session.refresh(group_image)
        return group_image


# @pytest.fixture(scope='session')
# async def post_image_fixture(post):
#     async with async_sessionmaker() as session:
#         post_image = PostImages(
#             urls=["https://example.com/post-image1.jpg", "https://example.com/post-image2.jpg"],
#             post_id=post.id,
#         )
#         session.add(post_image)
#         await session.commit()
#         await session.refresh(post_image)
#         return post_image


