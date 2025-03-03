
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OPENAI_TOKEN: str
    HOST: str

    @property
    def API_URL(self):
        return f"http://{self.HOST}:8000/images"

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()
