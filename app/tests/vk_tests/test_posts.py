import pytest
from app.tests.vk_tests.utils import get_fake_feed, get_response_mock
from vk.posts import load_user_feed


@pytest.mark.parametrize('posts_count', [1, 3, 4, 5, 10, 100])
async def test_load_user_feed_filters_ads(posts_count, mocker):
    fake_feed_data = get_fake_feed(posts_count=posts_count)
    fake_response = get_response_mock(fake_feed_data)
    mocker.patch(
        "httpx.AsyncClient.get",
        return_value=fake_response
    )

    posts = await load_user_feed(posts_count=posts_count)

    assert posts[0]["id"] == 1
    assert posts[0]["text"] == "Какой-то текст"
    assert not any(p for p in posts if p['marked_as_ads'] and len(p['text'] == 0))