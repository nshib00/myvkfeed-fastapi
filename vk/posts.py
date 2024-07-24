from httpx import AsyncClient

from vk.config import vk_settings


async def load_user_feed(posts_count: int = 50) -> list:
    vk_posts_url = f"https://api.vk.com/method/newsfeed.get?&access_token={vk_settings.api_token}&filters=post&count={posts_count}&v=5.131"
    async with AsyncClient() as client:
        posts_response = await client.get(url=vk_posts_url)
    posts = posts_response.json()["response"]["items"]
    clear_posts_from_ads(posts)
    return posts
    

def clear_posts_from_ads(posts: list) -> None:
    for post in posts:
        if post.get('marked_as_ads') == 1:
            posts.remove(post)



    