from httpx import AsyncClient

from app.config import settings


async def load_user_groups(user_id: int):
    vk_groups_url = f"https://api.vk.com/method/groups.get?access_token={settings.vk.API_TOKEN}&user_id={user_id}&extended=1&v=5.131"
    async with AsyncClient() as client:
        groups_response = await client.get(url=vk_groups_url)
        return groups_response.json()["response"]["items"]
    