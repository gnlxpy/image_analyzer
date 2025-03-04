
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OPENAI_TOKEN: str
    HOST: str
    OPENAI_SYSTEM: str
    PG_USER: str
    PG_PSW: str

    @property
    def API_URL(self):
        return f"http://{self.HOST}:8000/images"

    @property
    def PG_URL(self):
        return f'postgresql://{self.PG_USER}:{self.PG_PSW}@{self.HOST}:5432/postgres'

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()
