import traceback
import asyncpg
from config import settings
from pydantic import BaseModel, HttpUrl, Field
import datetime


class ResultAnalyzer(BaseModel):
    image_url: HttpUrl
    description: str = Field(min_length=30, max_length=5000)
    dt: datetime.datetime = Field(default_factory=datetime.datetime.now)


async def init_pg(loop):
    """
    Инициализация БД Постгрес
    :return: глобальная переменная с соединением
    """
    print('PG connected!')
    global pool
    pool = await asyncpg.create_pool(settings.PG_URL, loop=loop)
    return pool


async def close_pg():
    """
    Закрытие соединения
    """
    print('PG closed!')
    await pool.close()


class Pg:

    @staticmethod
    async def add_result(result: ResultAnalyzer) -> bool:
        try:
            async with pool.acquire() as conn:
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
                return True if r else False
        except Exception:
            traceback.print_exc()
            return False
