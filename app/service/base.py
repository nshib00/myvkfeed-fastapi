from sqlalchemy import Delete, Insert, MappingResult, Result, ScalarResult, Update, delete, insert, select, text, update

from app.database import async_sessionmaker


class BaseService:
    model = None

    @classmethod
    async def _get_result(cls, order_by_id: bool = False, **filters) -> ScalarResult:
        query = select(cls.model).filter_by(**filters)
        if order_by_id:
            query = query.order_by(cls.model.id)
        async with async_sessionmaker() as session:
            result = await session.execute(query)
            return result.scalars()
    
    @classmethod
    async def _execute_with_commit(cls, query: Insert | Update | Delete) -> Result:
        async with async_sessionmaker() as session:
            result = await session.execute(query)
            await session.commit()
        return result

    @classmethod
    async def find_all(cls, order_by_id: bool = False, **filters):
        result: ScalarResult = await cls._get_result(order_by_id, **filters)
        return result.all()
    
    @classmethod
    async def find_one_or_none(cls, **filters):
        result: ScalarResult = await cls._get_result(**filters)
        return result.one_or_none() 
        
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
    async def delete(cls, delete_condition=None, model=None) -> None:
        if cls.model is None:
            cls.model = model
        if delete_condition is not None:
            query = delete(cls.model).where(delete_condition)
        await cls._execute_with_commit(query)
    

    @classmethod
    async def delete_all(cls) -> None:
        query = text(f'TRUNCATE TABLE {cls.model.__tablename__} CASCADE')
        await cls._execute_with_commit(query)
    