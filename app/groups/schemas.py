from pydantic import BaseModel


class GroupSchema(BaseModel):
    id: int
    source_id: int
    title: str
    is_hidden: bool