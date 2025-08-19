import json
from httpx import Response


def get_fake_groups() -> dict:
    return {
        "response": {
            "count": 2,
            "items": [
                {
                    "id": 1234567,
                    "name": "Group 1",
                    "screen_name": "group1",
                    "is_closed": 0,
                    "type": "page",
                    "photo_50": "https://some-photo1",
                    "photo_100": "https://some-photo2",
                    "photo_200": "https://some-photo3"
                },
                {
                    "id": 234567890,
                    "name": "Group 2",
                    "screen_name": "group2",
                    "is_closed": 0,
                    "type": "page",
                    "photo_50": "https://some-photo1",
                    "photo_100": "https://some-photo2",
                    "photo_200": "https://some-photo3"
                },
            ]
        }
    }


def get_fake_feed(posts_count: int = 5) -> dict:
    feed_items = [
        {"id": 1, "text": "Какой-то текст", "attachments": ["photo"], "marked_as_ads": 0},
        {"id": 2, "text": "", "attachments": ["photo"], "marked_as_ads": 0},
        {"id": 3, "text": "Пост без вложений", "attachments": [], "marked_as_ads": 0},
        {"id": 4, "text": "Какая-то реклама", "attachments": ["photo"], "marked_as_ads": 1},
    ]

    if posts_count < len(feed_items):
        feed_items = feed_items[:posts_count]
    else:
        for post_id in range(5, posts_count + 1):
            feed_items.append(
                {"id": post_id, "text": f"Пост #{post_id}", "attachments": ["photo"], "marked_as_ads": 0},
            ) 

    return {
        "response": {
            "items": feed_items
        }
    } 


def get_response_mock(data) -> Response:
    return Response(
        status_code=200,
        content=json.dumps(data).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )


def get_fake_user_data() -> dict:
    return {
        'response': [
            {'id': 123456, 'first_name': 'Fake', 'last_name': 'User', 'can_access_closed': True, 'is_closed': False}
        ]
    }
     