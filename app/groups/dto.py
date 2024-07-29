from sqlalchemy import RowMapping
from app.groups.models import Groups
from app.images.models import GroupImages


class GroupDTO:
    @classmethod
    async def group_dict_to_model(cls, group_dict: dict, user_id: int) -> Groups:
        group_model = Groups(
            source_id=group_dict['id'],
            title=group_dict['name'], 
            is_hidden=False, 
            user_id=user_id,
        )
        group_model.group_image = GroupImages(url=group_dict['photo_50'])
        return group_model

    @classmethod
    async def raw_groups_to_models_list(cls, groups: list[dict], user_id: int) -> list[Groups]:
        group_models = []
        for group in groups:
            group_model = await cls.group_dict_to_model(group_dict=group, user_id=user_id)
            group_models.append(group_model)
        return group_models



    