from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Импорт конфига
    """
    OPENAI_TOKEN: str # токен openai
    HOST: str # адрес сервера
    OPENAI_SYSTEM: str # промт openai
    PG_USER: str # логин постгрес
    PG_PSW: str # пароль постгрес
    PG_HOST: str # адрес постгрес

    @property
    def API_URL(self):
        """
        Генерация ссылки на загруженные изображения
        """
        return f"http://{self.HOST}:8000/images"

    @property
    def PG_URL(self):
        """
        Генерация ссылки для логина в Постгрес
        """
        return f'postgresql://{self.PG_USER}:{self.PG_PSW}@{self.PG_HOST}:5432/postgres'

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()
