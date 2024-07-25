from sqlalchemy import insert, select

from app.database import Base, async_sessionmaker


class BaseService:
    model = None

    @classmethod
    async def __get_mapping_result(cls, **filters):
        query = select(cls.model.__table__.columns).filter_by(**filters)
        async with async_sessionmaker() as session:
            result = await session.execute(query)
            return result.mappings()

    @classmethod
    async def find_all(cls, **filters):
        result_mappings = await cls.__get_mapping_result(**filters)
        return result_mappings.all()
    
    @classmethod
    async def find_by_id(cls, model_id: int):
        result_mappings = await cls.__get_mapping_result(id=model_id)
        return result_mappings.one_or_none()
    
    @classmethod
    async def find_one_or_none(cls, **filters):
        result_mappings = await cls.__get_mapping_result(**filters)
        return result_mappings.one_or_none()
        
    @classmethod
    async def add(cls, **data):
        query = insert(cls.model).values(**data)
        async with async_sessionmaker() as session:
            await session.execute(query)
            await session.commit()


    # @classmethod
    # async def add_all_non_existing(cls, objects: list[Base], **filters) -> None:
    #     # Из всех переданных моделей добавляет в БД только те, которых еще нет.
    #     non_existing_objects = []
    #     async with async_sessionmaker() as session:
    #         for obj in objects:
    #             query = select(cls.model).filter_by(**filters)
    #             obj_from_db = await session.execute(query)
    #             if obj_from_db.one_or_none() is None:
    #                 non_existing_objects.append(obj)
    #         session.add_all(non_existing_objects)
    #         await session.commit()


    