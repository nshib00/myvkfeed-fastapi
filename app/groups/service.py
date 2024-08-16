from sqlalchemy import select
from app.groups.dto import GroupDTO
from app.groups.models import Groups
from app.images.models import GroupImages
from app.posts.models import Posts
from app.service.base import BaseService
from app.database import async_sessionmaker


class GroupService(BaseService):
    model = Groups

    @classmethod
    async def update(cls, update_condition, **values) -> int:
        updated_group_id = await BaseService.update(cls.model, update_condition, **values)
        return updated_group_id

    @classmethod
    async def add_groups_if_not_exist(cls, groups: list[Groups]) -> None:
        non_existing_groups = []
        async with async_sessionmaker() as session:
            for group in groups:
                group_query = select(Groups).where(Groups.source_id == group.source_id)
                group_from_db = await session.execute(group_query)
                if group_from_db.one_or_none() is None:
                    non_existing_groups.append(group)
            session.add_all(non_existing_groups)
            await session.commit()    

    @classmethod
    async def add_groups_list(cls, groups: list, user_id: int) -> None:
        group_models = GroupDTO.raw_groups_to_models_list(groups, user_id)
        await cls.add_groups_if_not_exist(group_models)

    @classmethod
    async def get_group_by_source_id(cls, source_id: int) -> Groups | None:
        group = await cls.find_one_or_none(source_id=source_id)
        return group

    @classmethod
    async def get_group_with_posts(cls, group_id: int) -> Groups | None:
        async with async_sessionmaker() as session:
            group_query = select(Groups).where(Groups.id == group_id)
            group_result = await session.execute(group_query)
            return group_result.scalar()
        
    @classmethod
    async def get_groups_with_images(cls, get_hidden: bool = False) -> list[Groups]:
        async with async_sessionmaker() as session:
            group_query = select(Groups).join(
                GroupImages, GroupImages.group_id == Groups.id
            ).where(Groups.is_hidden == get_hidden)
            group_result = await session.execute(group_query)
            return group_result.scalars().all()