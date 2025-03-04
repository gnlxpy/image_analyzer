import traceback
import asyncpg
from config import settings
from pydantic import BaseModel, HttpUrl, Field
import datetime


class ResultAnalyzer(BaseModel):
    """
    Модель результата анализа для БД
    """
    image_url: HttpUrl = Field(description='Ссылка на изображение')
    description: str = Field(min_length=30, max_length=5000, description='Описание')
    dt: datetime.datetime = Field(default_factory=datetime.datetime.now, description='отпечаток с датой и временем')


async def init_pg():
    """
    Инициализация соединения БД Постгрес
    """
    try:
        if len(settings.PG_USER) < 2:
            print('Pg off')
            return False
        conn = await asyncpg.connect(settings.PG_URL)
        return conn
    except Exception:
        return False


class Pg:

    @staticmethod
    async def add_result(result: ResultAnalyzer) -> bool:
        """
        Функция добавления строки в БД с ссылкой, описанием и отпечатком времени
        :param result: результат анализа для добавления
        :return: bool
        """
        try:
            conn = await init_pg()
            if not conn:
                print('Pg bad connection')
                return False
            r = await conn.fetch(
                '''
                INSERT INTO image_analyzer (image_url, description, dt)
                VALUES ($1, $2, $3)
                RETURNING id;
                ''',
                str(result.image_url),
                result.description,
                result.dt
            )
            await conn.close()
            return True if r else False
        except Exception:
            traceback.print_exc()
            return False
