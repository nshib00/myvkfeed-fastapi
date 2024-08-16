from pydantic import BaseModel


class ImageResponseSchema(BaseModel):
    urls: dict[str, str]