from pydantic import BaseModel


class ImageResponseSchema(BaseModel):
    url: str