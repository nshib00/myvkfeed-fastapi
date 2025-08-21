import asyncio
from faker import Faker
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from httpx import ASGITransport, AsyncClient
import pytest
from sqlalchemy import insert
from datetime import datetime

from app.database import Base, engine, async_sessionmaker
from app.config import settings
from app.tests.data.faker import dump_fake_data, load_fake_data
from app.main import app as fastapi_app

from app.users.auth.password_hash import HashPassword
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


@pytest.fixture(autouse=True, scope="session")
def init_cache():
    FastAPICache.init(InMemoryBackend(), prefix="test-cache")


@pytest.fixture(scope='function')
async def client():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url='http://test') as cli:
        yield cli


@pytest.fixture(scope='function')
async def faker():
    return Faker()


@pytest.fixture(scope='function')
async def test_user(faker):
    raw_password = 'password_test'
    async with async_sessionmaker() as session:
        new_user = Users(
            name=f'test_user_{faker.unique.user_name()}',
            vk_shortname=f'short_{faker.unique.user_name()}',
            hashed_password=HashPassword.get_password_hash(raw_password),
            date_joined=faker.date_time(),
            is_active=True,
            is_admin=False,
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
    return new_user, raw_password


@pytest.fixture(scope='function')
async def authenticated_client(test_user):
    user, raw_password = test_user
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app),
        base_url="http://test",
    ) as ac:
        resp = await ac.post(
            url="/auth/login",
            json={
                "name": user.name,
                "password": raw_password,
            },
        )
        assert resp.status_code == 200
        assert ac.cookies.get("myvkfeed_access_token") is not None
        yield ac


@pytest.fixture(scope='function')
async def admin_user(faker):
    raw_password = "admin_password"
    async with async_sessionmaker() as session:
        new_user = Users(
            name="admin_user",
            vk_shortname="admin_vk",
            hashed_password=HashPassword.get_password_hash(raw_password),
            is_active=True,
            is_admin=True,
            date_joined=faker.date_time()
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
    return new_user, raw_password


@pytest.fixture(scope='function')
async def admin_client(admin_user):
    user, password = admin_user
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url='http://test') as ac:
        resp = await ac.post(
            "/auth/login",
            json={"name": user.name, "password": password}
        )
        assert resp.status_code == 200
        assert ac.cookies.get("myvkfeed_access_token") is not None
        yield ac


@pytest.fixture(scope='function')
async def groups(test_user, faker):
    user, _ = test_user
    groups_data = [
        Groups(source_id=faker.unique.random_int(min=2000, max=9999), title="Group 1", user_id=user.id),
        Groups(source_id=faker.unique.random_int(min=2000, max=9999), title="Group 2", user_id=user.id),
        Groups(source_id=faker.unique.random_int(min=2000, max=9999), title="Hidden group 1", user_id=user.id, is_hidden=True),
        Groups(source_id=faker.unique.random_int(min=2000, max=9999), title="Hidden group 2", user_id=user.id, is_hidden=True),
    ]
    async with async_sessionmaker() as session:
        session.add_all(groups_data)
        await session.commit()
        for g in groups_data:
            await session.refresh(g)
    return groups_data


@pytest.fixture(scope='function')
async def group_images(groups):
    images = []
    async with async_sessionmaker() as session:
        for group in groups:
            group_image = GroupImages(
                url=f"https://example.com/group-image-{group.id}.jpg",
                group_id=group.id,
            )
            session.add(group_image)
            await session.commit()
            await session.refresh(group_image)
            images.append(group_image)
    return images


@pytest.fixture(scope='function')
async def test_post_with_image(groups, faker):
    post = Posts(
        pub_date=datetime.now(),
        vk_id=faker.unique.random_int(min=1000, max=9999),
        text="Post with image",
        group_id=groups[0].id,
    )
    image = PostImages(urls=["http://example.com/1.jpg"], post=post)

    async with async_sessionmaker() as session:
        session.add_all([post, image])
        await session.commit()

    return post


@pytest.fixture(scope='function')
async def posts(groups, faker):
    posts_data = [
        Posts(
            pub_date=datetime.now(),
            vk_id=faker.unique.random_int(min=1000, max=9999),
            text=f"Some post #{i}",
            group_id=groups[0].id,
        ) for i in range(1, 6)
    ]
    async with async_sessionmaker() as session:
        session.add_all(posts_data)
        await session.commit()
    return posts_data

