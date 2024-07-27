from datetime import datetime

from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    name: str
    password: str


class UserRegisterSchema(UserLoginSchema):
    vk_shortname: str


class UserResponseSchema(BaseModel):
    id: int
    name: str
    vk_shortname: str
    date_joined: datetime
    is_active: bool
