from httpx import AsyncClient

from app.config import settings


async def load_user_feed(posts_count: int = 50) -> list:
    vk_posts_url = f"https://api.vk.com/method/newsfeed.get?&access_token={settings.vk.API_TOKEN}&filters=post&count={posts_count}&v=5.131"
    async with AsyncClient() as client:
        posts_response = await client.get(url=vk_posts_url)
    posts = posts_response.json()["response"]["items"]
    clear_posts_from_ads(posts)
    return posts
    

def clear_posts_from_ads(posts: list) -> None:
    for post in posts:
        post_is_empty: bool = (not post.get('text')) or (not post.get('attachments'))
        if post.get('marked_as_ads') == 1 or post_is_empty:
            posts.remove(post)



    