import json


def save_posts_to_json(posts):
    with open("../../posts.json", "w", encoding="utf-8") as file:
        json.dump(posts, file, indent=4, ensure_ascii=False)


def load_posts_from_json():
    with open("../../posts.json", encoding="utf-8") as file:
        return json.load(file)
