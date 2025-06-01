from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn


class RunConfig(BaseModel):
    host: str = '0.0.0.0'
    port: int = 8000


class ApiPrefix(BaseModel):
    prefix: str = ''


class DatabaseConfig(BaseModel):
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    NAME: str

    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig


    @property
    def database_url(self) -> str:
        url: PostgresDsn = PostgresDsn(
            f'postgresql+asyncpg://'
            f'{self.db.DB_USER}:'
            f'{self.db.DB_PASSWORD}@'
            f'{self.db.DB_HOST}:'
            f'{self.db.DB_PORT}/'
            f'{self.db.DB_NAME}'
        )
        return str(url)

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
