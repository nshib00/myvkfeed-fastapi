from httpx import AsyncClient, Response

from vk.config import vk_settings


async def get_vk_user_response(vk_shortname: str) -> Response:
    vk_request_url = f"https://api.vk.com/method/users.get?&access_token={vk_settings.api_token}&user_ids={vk_shortname}&v=5.199"
    async with AsyncClient() as client:
        response = await client.get(url=vk_request_url)
    return response


async def get_vk_user_id_by_shortname(vk_shortname: str) -> int:
    response = await get_vk_user_response(vk_shortname)
    vk_user_id = response.json()["response"][0]['id']
    return vk_user_id


async def vk_user_profile_is_closed(vk_shortname: str) -> bool:
    response = await get_vk_user_response(vk_shortname)
    profile_is_closed = response.json()["response"][0]['is_closed']
    return profile_is_closed