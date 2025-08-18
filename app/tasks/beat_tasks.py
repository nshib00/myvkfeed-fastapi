from app.tasks.celery import celery_app
import asyncio
from app.users.auth.tokens.service import RefreshTokenService


@celery_app.task(name="clear_expired_refresh_tokens")
def clear_expired_refresh_tokens():
    asyncio.run(RefreshTokenService.delete_expired())