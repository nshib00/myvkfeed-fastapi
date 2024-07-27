from sqlalchemy import MappingResult, insert, select

from app.database import async_sessionmaker


class BaseService:
    model = None

    @classmethod
    async def __get_mapping_result(cls, **filters) -> MappingResult:
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
    async def add(cls, **data) -> int:
        query = insert(cls.model).values(**data).returning(cls.model.id)
        async with async_sessionmaker() as session:
            result = await session.execute(query)
            await session.commit()
        return result.scalar()


    