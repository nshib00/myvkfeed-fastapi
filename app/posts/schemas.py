import datetime
from pydantic import BaseModel


class PostSchema(BaseModel):
    id: int
    pub_date: datetime.datetime
    vk_id: int
    group_id: int | None
    text: str