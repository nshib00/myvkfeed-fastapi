from app.groups.models import Groups
from app.images.models import GroupImages, PostImages
from app.posts.models import Posts
from app.users.models import Users

from sqladmin import ModelView


class UsersAdmin(ModelView, model=Users):
    can_delete = False
    icon = 'fa-solid fa-people-line'
    name = 'Пользователь'
    name_plural = 'Пользователи'

    column_exclude_list = [Users.hashed_password, 'groups']
    column_details_exclude_list = [Users.hashed_password]


class GroupsAdmin(ModelView, model=Groups):
    can_delete = False
    name = 'Группа'
    name_plural = 'Группы'

    column_list = [
        Groups.id, 'user', Groups.title, Groups.is_hidden, 'group_image'
    ]



class PostsAdmin(ModelView, model=Posts):
    can_delete = False
    name = 'Пост'
    name_plural = 'Посты'

    column_list = [
        Posts.id, 'group', Posts.pub_date, Posts.text, 'images'
    ]


class PostImagesAdmin(ModelView, model=PostImages):
    can_delete = False
    name = 'Картинка из поста'
    name_plural = 'Картинки из постов'
    icon = 'fa-solid fa-image'

    column_list = [PostImages.id, 'post']


class GroupImagesAdmin(ModelView, model=GroupImages):
    can_delete = False
    name = 'Аватарка группы'
    name_plural = 'Аватарки групп'
    icon = 'fa-solid fa-png'

    column_list = [GroupImages.id, 'group']



ALL_ADMIN_VIEWS = (UsersAdmin, GroupsAdmin, PostsAdmin, PostImagesAdmin, GroupImagesAdmin)


