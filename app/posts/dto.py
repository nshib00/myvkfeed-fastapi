from datetime import datetime
from sqlalchemy.exc import InvalidRequestError

from app.groups.service import GroupService
from app.images.models import PostImages
from app.posts.models import Posts
from app.posts.schemas import PostResponseRenderSchema, PostResponseSchemaWithImages
from app.images.schemas import ImageResponseSchema


class PostDTO:

    @classmethod
    async def post_dict_to_model(cls, post_dict: dict) -> Posts:
        post_source_id = post_dict['source_id']
        post_model = Posts(
            pub_date=datetime.fromtimestamp(post_dict['date']),
            vk_id=post_dict['id'],
            text=post_dict['text'],
        )
        post_model.images = cls.get_images_from_post_dict(post_dict)
        post_group = await GroupService.get_group_by_source_id(
            source_id=-post_source_id
        )
        try:
            post_model.group = post_group 
        except InvalidRequestError:
            print(f'Cannot attach group: {post_group}.\nPost text: {post_model.text[:20] + "..."}')
        return post_model
    

    @classmethod
    def get_images_from_post_dict(cls, post_dict: dict) -> list[PostImages]:
        post_images = []

        for attachment in post_dict.get('attachments'):
            if attachment['type'] == 'photo':
                post_images.append(
                    PostImages(
                        url=attachment['photo']['orig_photo']['url']
                    )
                )
        return post_images


    @classmethod
    async def raw_posts_to_models_list(cls, posts: list[dict]) -> list[Posts]:
        post_models = []
        for post in posts:
            post_model = await cls.post_dict_to_model(post_dict=post)
            post_models.append(post_model)
        return post_models


    @classmethod
    def one_model_to_schema(cls, post_model: Posts, with_group_title=False) -> PostResponseRenderSchema:
        post_schema = PostResponseRenderSchema(
            id=post_model.id,
            pub_date=post_model.pub_date,
            text=post_model.text,
            group_id=post_model.group_id,
            images=[
                ImageResponseSchema(url=img.url) for img in post_model.images
            ],
            group_title=None
        )
        if with_group_title:
            if hasattr(post_model.group, 'title'):
                post_schema.group_title = post_model.group.title
        return post_schema
    
    @classmethod
    def many_models_to_schemas(cls, post_models: list[Posts], with_group_title=False) -> list[PostResponseRenderSchema]:
        return [
            cls.one_model_to_schema(post_model, with_group_title=with_group_title) for post_model in post_models
        ]
