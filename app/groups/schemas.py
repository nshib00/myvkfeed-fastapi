from typing import Any
from pydantic import BaseModel

from app.posts.models import Posts


class GroupSchema(BaseModel):
    id: int
    source_id: int
    title: str
    is_hidden: bool
    user_id: int


class GroupSchemaWithPosts(GroupSchema):
    posts: list = []
