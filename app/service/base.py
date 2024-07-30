from sqlalchemy import Delete, Insert, MappingResult, Result, Update, delete, insert, select, text, update

from app.database import async_sessionmaker


class BaseService:
    model = None

    @classmethod
    async def _get_result(cls, **filters) -> Result:
        query = select(cls.model).filter_by(**filters)
        async with async_sessionmaker() as session:
            result = await session.execute(query)
            return result
        

    @classmethod
    async def _get_mapping_result(cls, **filters) -> MappingResult:
        query = select(cls.model.__table__.columns).filter_by(**filters)
        async with async_sessionmaker() as session:
            result = await session.execute(query)
            return result.mappings()
    

    @classmethod
    async def _get_all_result(cls, **filters):
        result = await cls._get_result(**filters)
        return result.all()
    

    @classmethod
    async def _get_scalars_result(cls, **filters):
        result = await cls._get_result(**filters)
        return result.scalars()


    @classmethod
    async def _execute_with_commit(cls, query: Insert | Update | Delete) -> Result:
        async with async_sessionmaker() as session:
            result = await session.execute(query)
            await session.commit()
        return result

    @classmethod
    async def find_all(cls, **filters):
        result_mappings = await cls._get_mapping_result(**filters)
        return result_mappings.all()
    
    @classmethod
    async def find_by_id(cls, model_id: int):
        result_mappings = await cls._get_mapping_result(id=model_id)
        return result_mappings.one_or_none()
    
    @classmethod
    async def find_one_or_none(cls, mode: str = 'mappings', **filters):
        if mode == 'mappings':
            result_mappings = await cls._get_mapping_result(**filters)
            return result_mappings.one_or_none()
        if mode == 'scalars':
            result_scalars = await cls._get_scalars_result(**filters)
            return result_scalars.one_or_none()
        if mode == 'all':
            result = await cls._get_all_result(**filters)
            return result
        
        
    @classmethod
    async def add(cls, **data) -> int:
        query = insert(cls.model).values(**data).returning(cls.model.id)
        result = await cls._execute_with_commit(query)
        return result.scalar()
    

    @classmethod
    async def update(cls, model, update_condition, **values) -> int:
        query = update(model).where(update_condition).values(**values).returning(model.id)
        result = await cls._execute_with_commit(query)
        return result.scalar()
    

    @classmethod
    async def delete(cls, delete_condition=None) -> int:
        if delete_condition is not None:
            query = delete(cls.model).where(delete_condition).returning(cls.model.id)
        result = await cls._execute_with_commit(query)
        return result.scalar()
    

    @classmethod
    async def delete_all(cls) -> None:
        query = text(f'TRUNCATE TABLE {cls.model.__tablename__} CASCADE')
        await cls._execute_with_commit(query)
    