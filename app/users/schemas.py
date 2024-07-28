from datetime import datetime

from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    name: str
    password: str


class UserRegisterSchema(UserLoginSchema):
    vk_shortname: str


class ShortUserResponseSchema(BaseModel):
    id: int
    name: str
    vk_shortname: str


class UserResponseSchema(ShortUserResponseSchema):
    date_joined: datetime
    is_active: bool
    is_admin: bool
