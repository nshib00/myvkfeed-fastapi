from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import IntEnum
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class PostLimit(IntEnum):
    TINY = 100
    SMALL = 500
    MEDIUM = 1000
    LARGE = 2500
    VERY_LARGE = 5000


class BaseAppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8"
    )


class TestSettings(BaseAppSettings):
    model_config = {
        **BaseAppSettings.model_config,
        'env_prefix': 'TEST_'
    }

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PWD: str
    DB_NAME: str

    @property
    def db_url(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PWD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


class VKSettings(BaseAppSettings):
    model_config = {
        **BaseAppSettings.model_config,
        'env_prefix': 'VK_'
    }

    API_TOKEN: str
    

class DBSettings(BaseAppSettings):
    model_config = {
        **BaseAppSettings.model_config,
        'env_prefix': 'DB_'
    }

    HOST: str
    PORT: int
    USER: str
    PWD: str
    NAME: str

    @property
    def url(self):
        return f'postgresql+asyncpg://{self.USER}:{self.PWD}@{self.HOST}:{self.PORT}/{self.NAME}'


class AppSettings(BaseAppSettings):
    posts_limit: IntEnum = PostLimit.MEDIUM


class AuthSettings(BaseAppSettings):
    SECRET_KEY: str | None = None
    ALGORITHM: str | None = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 60


class RedisSettings(BaseAppSettings):
    model_config = {
        **BaseAppSettings.model_config,
        'env_prefix': 'REDIS_'
    }

    URL: str | None = None


class CelerySettings(BaseAppSettings):
    broker_url: str = Field(..., alias='CELERY_BROKER_URL')


class Settings(BaseSettings):
    mode: str = Field(..., alias='MODE')
    
    db: DBSettings = DBSettings()
    vk: VKSettings = VKSettings()
    auth: AuthSettings = AuthSettings()
    app: AppSettings = AppSettings()
    redis: RedisSettings = RedisSettings()
    celery: CelerySettings = CelerySettings()
    

settings = Settings()
test_settings = TestSettings()