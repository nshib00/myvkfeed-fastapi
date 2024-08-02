from app.service.base import BaseService
from app.users.auth.tokens.models import RefreshTokens


class RefreshTokenService(BaseService):
    model = RefreshTokens

    @classmethod
    async def delete(cls, token_user_id: int) -> None:
        await BaseService.delete(
            model=cls.model,
            delete_condition=RefreshTokens.user_id == token_user_id
        )