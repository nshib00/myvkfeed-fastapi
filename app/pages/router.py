from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.groups.router import get_all_groups_to_render, get_group_by_id
from app.groups.schemas import GroupSchema, GroupSchemaWithPosts
from app.posts.router import get_all_posts_to_render, get_post_by_id
from app.posts.schemas import PostResponseRenderSchema, PostResponseSchemaWithImages


router = APIRouter(
    prefix='/pages',
    tags=['HTML-страницы']
)

templates = Jinja2Templates(directory='app/templates')


@router.get('')
async def get_main_page(request: Request, posts: list[PostResponseRenderSchema] = Depends(get_all_posts_to_render)):
    return templates.TemplateResponse(
        name='index.html',
        context={
            'request': request,
            'posts': posts,
        }
    )

@router.get('/post/{post_id}')
async def get_post_page(request: Request, post: PostResponseRenderSchema = Depends(get_post_by_id)):
    return templates.TemplateResponse(
        name='post.html',
        context={
            'request': request,
            'post': post,
        }
    )


@router.get('/groups')
async def get_all_groups_page(request: Request, groups: list[GroupSchema] = Depends(get_all_groups_to_render)):
    return templates.TemplateResponse(
        name='all_groups.html',
        context={
            'request': request,
            'groups': groups,
        }
    )


@router.get('/group/{group_id}')
async def get_group_page(
    request: Request, group: GroupSchemaWithPosts = Depends(get_group_by_id)
):
    return templates.TemplateResponse(
        name='group.html',
        context={
            'request': request,
            'group': group,
        }
    )