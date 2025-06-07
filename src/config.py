from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn


class RunConfig(BaseModel):
    host: str
    port: int


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

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig

    @property
    def database_url(self) -> str:
        url: PostgresDsn = PostgresDsn(
            f'postgresql+asyncpg://'
            f'{self.db.USER}:'
            f'{self.db.PASSWORD}@'
            f'{self.db.HOST}:'
            f'{self.db.PORT}/'
            f'{self.db.NAME}'
        )
        return str(url)

    model_config = SettingsConfigDict(
        env_file=('.env-template', '.env'),
        case_sensitive=False,
        env_prefix='TFIDF__',
        env_nested_delimiter='__',
    )


settings = Settings()
