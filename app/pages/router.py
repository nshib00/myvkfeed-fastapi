from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.groups.router import add_all_groups, get_all_groups_to_render, get_group_by_id
from app.groups.schemas import GroupSchema, GroupSchemaWithPosts
from app.posts.router import add_all_posts, get_all_posts_to_render, get_post_by_id
from app.posts.schemas import PostResponseRenderSchema
from app.users.auth.dependencies import get_active_current_user
from app.users.models import Users
from app import __version__


router = APIRouter(
    prefix='/pages',
    tags=['HTML-страницы']
)

templates = Jinja2Templates(directory='app/templates')


base_context = {
    'menu': [
        {'title': 'Обновить ленту', 'url': '/pages/update_feed'},
        {'title': 'Мои группы', 'url': '/pages/groups'},
    ],
    'version': __version__,
    'year': '2024',
}


@router.get('')
async def get_main_page(
    request: Request,
    posts: list[PostResponseRenderSchema] = Depends(get_all_posts_to_render),
    user: Users = Depends(get_active_current_user)
):
    return templates.TemplateResponse(
        name='index.html',
        context=base_context | {
            'request': request,
            'posts': posts,
            'user': user,
        }
    )

@router.get('/post/{post_id}')
async def get_post_page(
    request: Request,
    post: PostResponseRenderSchema = Depends(get_post_by_id),
    user: Users = Depends(get_active_current_user)
):
    return templates.TemplateResponse(
        name='post.html',
        context=base_context | {
            'request': request,
            'post': post,
            'user': user,
        }
    )


@router.get('/groups')
async def get_all_groups_page(
    request: Request,
    groups: list[GroupSchema] = Depends(get_all_groups_to_render),
    user: Users = Depends(get_active_current_user)
):
    return templates.TemplateResponse(
        name='all_groups.html',
        context=base_context | {
            'request': request,
            'groups': groups,
            'user': user,
        }
    )


@router.get('/group/{group_id}')
async def get_group_page(
    request: Request,
    group: GroupSchemaWithPosts = Depends(get_group_by_id),
    user: Users = Depends(get_active_current_user)
):
    return templates.TemplateResponse(
        name='group.html',
        context=base_context | {
            'request': request,
            'group': group,
            'user': user,
        }
    )


@router.get('/update_feed')
async def get_group_page(
    request: Request,
    added_groups = Depends(add_all_groups),
    added_posts = Depends(add_all_posts),
    user: Users = Depends(get_active_current_user)
):
    return RedirectResponse(url='/pages', status_code=status.HTTP_303_SEE_OTHER)