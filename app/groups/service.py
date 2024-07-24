from sqlalchemy import select
from app.groups.dto import GroupDTO
from app.groups.models import Groups
from app.service.base import BaseService
from app.database import async_sessionmaker


class GroupService(BaseService):
    model = Groups


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
    async def add_groups_list(cls, groups: list) -> None:
        group_models = await GroupDTO.raw_groups_to_models_list(groups)
        await cls.add_groups_if_not_exist(group_models)
    