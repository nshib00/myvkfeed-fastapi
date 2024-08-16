from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import IntEnum


class PostLimit(IntEnum):
    TINY = 100
    SMALL = 500
    MEDIUM = 1000
    LARGE = 2500
    VERY_LARGE = 5000


class VKSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='VK_')

    API_TOKEN: str
    

class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='DB_')

    HOST: str
    PORT: int
    USER: str
    PWD: str
    NAME: str

    @property
    def URL(self):
        return f'postgresql+asyncpg://{self.USER}:{self.PWD}@{self.HOST}:{self.PORT}/{self.NAME}'


class AppSettings(BaseSettings):
    posts_limit: IntEnum = PostLimit.MEDIUM


class AuthSettings(BaseSettings):
    SECRET_KEY: str | None = None
    ALGORITHM: str | None = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 60


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='REDIS_')

    URL: str | None = None


class Settings(BaseSettings):
    db: DBSettings = DBSettings()
    vk: VKSettings = VKSettings()
    auth: AuthSettings = AuthSettings()
    app: AppSettings = AppSettings()
    redis: RedisSettings = RedisSettings()
    
    class Config:
        env_file = '../.env'


settings = Settings()