from app.groups.models import Groups
from app.groups.schemas import GroupSchemaWithPosts
from app.images.models import GroupImages
from app.images.schemas import ImageResponseSchema
from app.posts.schemas import PostResponseSchemaWithImages


class GroupDTO:
    @classmethod
    def group_dict_to_model(cls, group_dict: dict, user_id: int) -> Groups:
        group_model = Groups(
            source_id=group_dict['id'],
            title=group_dict['name'], 
            is_hidden=False, 
            user_id=user_id,
        )
        group_model.group_image = GroupImages(url=group_dict['photo_50'])
        return group_model

    @classmethod
    def raw_groups_to_models_list(cls, groups: list[dict], user_id: int) -> list[Groups]:
        group_models = []
        for group in groups:
            group_model = cls.group_dict_to_model(group_dict=group, user_id=user_id)
            group_models.append(group_model)
        return group_models
    
    @classmethod
    def model_to_schema(cls, group_model: Groups) -> GroupSchemaWithPosts:
        return GroupSchemaWithPosts(
        id=group_model.id,
        title=group_model.title,
        source_id=group_model.source_id,
        is_hidden=group_model.is_hidden,
        user_id=group_model.user_id,
        posts=[
            PostResponseSchemaWithImages(
                id=post.id,
                pub_date=post.pub_date,
                text=post.text,
                images=[
                    ImageResponseSchema(url=img.url) for img in post.images
                ]
             ) for post in group_model.posts
        ],
    )



    