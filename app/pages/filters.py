from datetime import datetime

from app.images.schemas import ImageResponseSchema


def format_datetime(date: datetime | str) -> datetime:
    if isinstance(date, datetime):
        return date.strftime('%d.%m.%Y %H:%M')
    date_str = date.replace('T', ' ')
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M')


def choose_optimal_image_url(image: dict | ImageResponseSchema, images_in_post: int) -> str:
    if isinstance(image, ImageResponseSchema):
        image_urls = image.urls
    elif isinstance(image, dict):
        image_urls = image['urls']

    if images_in_post >= 5:
        return image_urls.get('p') or image_urls.get('q')
    elif 2 <= images_in_post <= 4:
        return image_urls.get('q') or image_urls.get('r')
    return image_urls.get('r')
    