from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.posts.router import get_all_posts, get_all_posts_with_related_data, get_post_by_id
from app.posts.schemas import PostResponseSchemaWithImages


router = APIRouter(
    prefix='/pages',
    tags=['HTML-страницы']
)

templates = Jinja2Templates(directory='app/templates')


@router.get('')
async def get_main_page(request: Request, posts: list[PostResponseSchemaWithImages] = Depends(get_all_posts_with_related_data)):
    return templates.TemplateResponse(
        name='index.html',
        context={
            'request': request,
            'posts': posts,
        }
    )

@router.get('/post/{post_id}')
async def get_post_page(request: Request, post: PostResponseSchemaWithImages = Depends(get_post_by_id)):
    return templates.TemplateResponse(
        name='post.html',
        context={
            'request': request,
            'post': post,
        }
    )