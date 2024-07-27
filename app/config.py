from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PWD: str
    VK_API_TOKEN: str
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = '.env'

    @property
    def DB_URL(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PWD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


settings = Settings()

# TODO: сделать post_limit (по умолчанию 1000) - столько постов максимально сможет храниться у юзера.
# сделать возможным изменять post_limit до 500, 2500, 5000