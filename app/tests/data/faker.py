import json
import random
from faker import Faker
from pathlib import Path


faker_obj = Faker()


def make_fake_post() -> dict:
    return {
        'pub_date': str(faker_obj.date_time()),
        'vk_id': random.randint(1000000, 2000000),
        'text': faker_obj.text(max_nb_chars=200)
    }


def make_fake_group(fake_user_id: int) -> dict:
    return {
        'source_id': random.randint(1000000, 2000000),
        'title': faker_obj.country(),
        'is_hidden': random.choice([True, False]),
        'user_id': fake_user_id,
    }


def make_fake_user(is_admin: bool = False) -> dict:
    return {
        'name': faker_obj.name(),
        'vk_shortname': faker_obj.first_name().lower(),
        'hashed_password': faker_obj.sha256(),
        'date_joined': str(faker_obj.date_time()),
        'is_active': True,
        'is_admin': is_admin,
    }


def get_data_dir_path() -> Path:
    return Path('app/tests/data')


def dump_fake_data(users_count=5, posts_count=10, groups_count=10):
    data_dir_path = get_data_dir_path()

    filenames = ('fake_users.json', 'fake_groups.json', 'fake_posts.json')
    if all(Path(fname).exists() for fname in filenames):
        return

    fake_users = [
        make_fake_user() for _ in range(users_count - 1)
    ] + [make_fake_user(is_admin=True)]
    fake_posts = [make_fake_post() for _ in range(posts_count)]
    fake_groups = [
        make_fake_group(fake_user_id=random.randint(1, users_count)) for _ in range(groups_count)
    ]

    for filename, fake_obj in zip(filenames, [fake_users, fake_groups, fake_posts]):
        with open(data_dir_path / filename, 'w', encoding='utf-8') as file:
            json.dump(fake_obj, file, ensure_ascii=False, indent=4)


def load_fake_data(model: str, count: int | None = None):
    data_dir_path = get_data_dir_path()
    with open(data_dir_path / f'fake_{model}.json') as file:
        fake_data = json.load(file)
    if count is None:
        return fake_data
    return fake_data[:count]