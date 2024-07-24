from app.posts.models import Posts
from app.service.base import BaseService


class PostService(BaseService):
    model = Posts