from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings, test_settings


if settings.mode == 'test':
    db_url = test_settings.db_url
    db_params = {'poolclass': NullPool}
else:
    db_url = settings.db.url
    db_params = {}


engine = create_async_engine(url=db_url, **db_params)
async_sessionmaker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass