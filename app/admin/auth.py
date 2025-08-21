from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.config import settings
from app.users.auth.dependencies import get_current_user
from app.users.auth.logic import authenticate_user, create_access_and_refresh_tokens


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        user = await authenticate_user(username, password)
        if user is None:
            return False
        
        user_token_data = {'sub': user.id}
        tokens = create_access_and_refresh_tokens(token_data=user_token_data)

        request.session.update(
            {"access_token": tokens.access_token, "refresh_token": tokens.refresh_token}
        )

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False
        
        user = await get_current_user(token)
        if user is None:
            return False
        
        return True


admin_auth_backend = AdminAuth(secret_key=settings.db.url)