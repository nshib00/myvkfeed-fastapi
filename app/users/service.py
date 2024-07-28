from app.service.base import BaseService
from app.users.models import Users


class UserService(BaseService):
    model = Users

    @classmethod
    async def update(cls, username: str, **values) -> int:
        update_condition = cls.model.name == username
        updated_field_id = await BaseService.update(cls.model, update_condition, **values)
        return updated_field_id