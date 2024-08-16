from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as aioredis
import uvicorn

from users.router import router as users_router
from users.auth.router import router as auth_router
from posts.router import router as posts_router
from groups.router import router as groups_router
from images.router import router as images_router
from pages.router import router as pages_router

from config import settings


async def app_lifespan(_: FastAPI):
    redis_client = aioredis.from_url(settings.redis.URL)
    FastAPICache.init(backend=RedisBackend(redis_client), prefix='myvkfeed-cache')
    yield


app = FastAPI(lifespan=app_lifespan)
app.mount('/static', StaticFiles(directory='app/static'), 'static')


for router in (users_router, posts_router, groups_router, images_router, auth_router, pages_router):
    app.include_router(router)


if __name__ == '__main__':
    uvicorn.run('main:app', port=12500, reload=True)
 