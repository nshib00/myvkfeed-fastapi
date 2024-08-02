from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.posts.router import get_all_posts
from app.posts.schemas import PostSchema


router = APIRouter(
    prefix='/pages',
    tags=['HTML-страницы']
)

templates = Jinja2Templates(directory='app/templates')


@router.get('')
async def get_main_page(request: Request, posts: list[PostSchema] = Depends(get_all_posts)):
    return templates.TemplateResponse(
        name='index.html',
        context={'request': request, 'posts': posts}
    )