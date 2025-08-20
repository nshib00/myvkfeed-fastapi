import pytest
from datetime import datetime
from app.posts.service import PostService
from app.posts.models import Posts
    

async def test_add_posts_list(posts):
    await PostService.add_posts_list(posts)

    for i in range(len(posts)):
        post_from_db = await PostService.find_one_or_none(vk_id=posts[i].vk_id)
        assert post_from_db is not None
        assert post_from_db.text == posts[i].text

    
async def test_get_post_with_images(test_post_with_image):
    post = await PostService.get_post_with_images(test_post_with_image.id)
    assert post is not None
    assert len(post.images) == 1
    assert "example.com" in post.images[0].urls[0]


@pytest.mark.parametrize("order_by_pub_date", [True, False])
async def test_get_posts_with_group_and_images(test_post_with_image, order_by_pub_date: bool):
    posts = await PostService.get_posts_with_group_and_images(order_by_pub_date=order_by_pub_date)
    
    assert isinstance(posts, list)
    assert any(p for p in posts if p.id == test_post_with_image.id)
    
    for post in posts:
        assert post.group is not None
        assert all(isinstance(img.urls, list) for img in post.images)

    if order_by_pub_date and len(posts) > 1:
        pub_dates = [p.pub_date for p in posts]
        assert pub_dates == sorted(pub_dates, reverse=True)


async def test_find_non_existing_posts():
    posts_list = [
        # существующие посты
        Posts(vk_id=201, pub_date=datetime.now(), text="Existing post 1", group_id=1),
        Posts(vk_id=202, pub_date=datetime.now(), text="Existing post 2", group_id=1),

        # несуществующие посты
        Posts(vk_id=999, pub_date=datetime.now(), text="Non-existing post 1", group_id=1),
        Posts(vk_id=1000, pub_date=datetime.now(), text="Non-existing post 2", group_id=1),
        Posts(vk_id=1001, pub_date=datetime.now(), text="Non-existing post 3", group_id=1),
    ]
    vk_ids = [post.vk_id for post in posts_list if post.text.startswith("Non-")] 
    non_existing_posts = await PostService.find_non_existing_posts(posts_list=posts_list)

    assert len(non_existing_posts) == 3
    assert [p.vk_id for p in non_existing_posts] == vk_ids
