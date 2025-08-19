import json
from httpx import Response
from app.tests.vk_tests.utils import get_fake_groups, get_response_mock
from vk.groups import load_user_groups


async def test_load_user_groups(mocker):
    fake_data = get_fake_groups()
    fake_response = get_response_mock(fake_data)

    mocker.patch(
        'httpx.AsyncClient.get',
        return_value=fake_response
    )
    user_groups = await load_user_groups(user_id=1)

    assert len(user_groups) == 2

    group_names = ('Group 1', 'Group 2')
    for index, group in enumerate(user_groups):
        assert 'id' in group
        assert 'name' in group
        assert group['name'] == group_names[index]
        assert 'is_closed' in group
        assert 'type' in group
        


