import datetime
from typing import Any
from pydantic import BaseModel


class PostResponseSchema(BaseModel):
    id: int
    pub_date: datetime.datetime
    text: str


class PostResponseSchemaWithImages(PostResponseSchema):
    images: list = []


class PostSchema(PostResponseSchema):
    vk_id: int
    group_id: int | None


class PostResponseRenderSchema(PostResponseSchemaWithImages):
    group_title: str | None



    
