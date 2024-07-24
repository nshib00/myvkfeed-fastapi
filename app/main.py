from fastapi import FastAPI
import uvicorn

from users.router import router as users_router
from posts.router import router as posts_router
from groups.router import router as groups_router
from images.router import router as images_router


app = FastAPI()

for router in (users_router, posts_router, groups_router, images_router):
    app.include_router(router)


if __name__ == '__main__':
    uvicorn.run('main:app', port=12500, reload=True)
