from httpx import AsyncClient

from vk.config import vk_settings


async def load_user_groups(user_id: int):
    vk_groups_url = f"https://api.vk.com/method/groups.get?access_token={vk_settings.api_token}&user_id={user_id}&extended=1&v=5.131"
    async with AsyncClient() as client:
        groups_response = await client.get(url=vk_groups_url)
        return groups_response.json()["response"]["items"]
    