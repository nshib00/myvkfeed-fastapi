import pytest
from httpx import Response
from app.tests.vk_tests.utils import get_response_mock, get_fake_user_data
from vk.users import get_vk_user_response, get_vk_user_id_by_shortname, vk_user_profile_is_closed



async def test_get_vk_user_response(mocker):
    vk_shortname = 'somename'
    fake_data = get_fake_user_data()
    fake_response = get_response_mock(fake_data)
    mocker.patch('httpx.AsyncClient.get', return_value=fake_response)

    user_response = await get_vk_user_response(vk_shortname)
    
    assert user_response.status_code == 200
    assert len(user_response.json()['response']) == 1
    assert user_response.json()['response'][0]['id'] == 123456


async def test_get_vk_user_id_by_shortname(mocker):
    vk_shortname = 'somename'
    fake_data = get_fake_user_data()
    fake_response = get_response_mock(fake_data)
    mocker.patch('httpx.AsyncClient.get', return_value=fake_response)
    
    user_id = await get_vk_user_id_by_shortname(vk_shortname)
    assert user_id == 123456


async def test_vk_user_profile_is_closed(mocker):
    vk_shortname = 'somename'
    fake_data = get_fake_user_data()
    fake_response = get_response_mock(fake_data)
    mocker.patch('httpx.AsyncClient.get', return_value=fake_response)

    is_closed = await vk_user_profile_is_closed(vk_shortname)
    assert is_closed is False