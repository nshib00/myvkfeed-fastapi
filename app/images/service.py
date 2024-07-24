from app.images.models import GroupImages, PostImages
from app.service.base import BaseService


class PostImageService(BaseService):
    model = PostImages


class GroupImageService(BaseService):
    model = GroupImages