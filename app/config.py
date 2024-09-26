import os

from pydantic import computed_field, RedisDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class Settings(BaseSettings):
    WEBSERVER_HOST: str
    WEBSERVER_PORT: str

    REDIS_HOST: str
    REDIS_PORT: int


    @computed_field
    @property
    def redis_url(self) -> RedisDsn:
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}'
    
    model_config = SettingsConfigDict(env_file=DOTENV)


settings = Settings()
