from typing import Any
from pydantic import BaseModel


class GroupSchema(BaseModel):
    id: int
    source_id: int
    title: str
    is_hidden: bool
    user_id: int


class GroupSchemaWithPosts(GroupSchema):
    posts: list = []


class ImageGroupSchema(GroupSchema):
    image: Any


class GroupRenderSchema(ImageGroupSchema, GroupSchemaWithPosts):
    pass