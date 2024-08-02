from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from users.router import router as users_router
from users.auth.router import router as auth_router
from posts.router import router as posts_router
from groups.router import router as groups_router
from images.router import router as images_router
from pages.router import router as pages_router


app = FastAPI()
app.mount('/static', StaticFiles(directory='app/static'), 'static')

for router in (users_router, posts_router, groups_router, images_router, auth_router, pages_router):
    app.include_router(router)


if __name__ == '__main__':
    uvicorn.run('main:app', port=12500, reload=True)
 