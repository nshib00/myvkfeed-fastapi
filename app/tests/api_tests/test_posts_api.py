from datetime import datetime

from app.database import async_sessionmaker
from app.posts.models import Posts
from app.main import app as fastapi_app


async def test_get_all_posts(authenticated_client, posts):
    ac = authenticated_client
    response = await ac.get("/posts")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert list(reversed([p['vk_id'] for p in data])) == [p.vk_id for p in posts]


async def test_get_post_by_id(authenticated_client, posts):
    ac = authenticated_client
    post = posts[0]
    response = await ac.get(f"/posts/post/{post.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == post.id
    assert "group_title" in data


async def test_load_user_posts_from_vk(authenticated_client, mocker):  
    ac = authenticated_client
    fake_vk_feed = [
        {"vk_id": 8888, "text": "VK feed post", "pub_date": datetime.now()}
    ]
    mocker.patch("app.posts.router.load_user_feed", new_callable=mocker.AsyncMock, return_value=fake_vk_feed)
    response = await ac.get("/posts/load")   
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


async def test_add_all_posts(authenticated_client, groups, mocker):
    ac = authenticated_client
    fake_vk_posts = [
        {"vk_id": 9999, "text": "New VK post", "pub_date": datetime.now()}
    ]
    mocker.patch(
        "vk.posts.load_user_feed",
        new_callable=mocker.AsyncMock,
        return_value=fake_vk_posts
    )

    response = await ac.post("/posts")
    assert response.status_code in (200, 201)
    data = response.json()
    assert "added_posts_count" in data
    assert data["added_posts_count"] > 0


async def test_delete_all_posts(admin_client, authenticated_client):
    admin_ac = admin_client
    ac = authenticated_client

    user_response = await ac.delete("/posts")
    assert user_response.status_code == 403

    admin_response = await admin_ac.delete("/posts")
    assert admin_response.status_code == 204
    
    # проверяем, что в БД больше нет постов
    async with async_sessionmaker() as session:
        all_posts = await session.execute(Posts.__table__.select())
        all_posts_fetched = all_posts.fetchall()
    assert len(all_posts_fetched) == 0


async def test_get_post_not_exists(authenticated_client):
    ac = authenticated_client
    response = await ac.get("/posts/post/999999")
    assert response.status_code == 404