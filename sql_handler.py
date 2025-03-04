import asyncio
import traceback
import asyncpg
from config import settings
from pydantic import BaseModel, HttpUrl, Field
import datetime


class ResultAnalyzer(BaseModel):
    image_url: HttpUrl
    description: str = Field(min_length=30, max_length=5000)
    dt: datetime.datetime = Field(default_factory=datetime.datetime.now)


async def init_pg():
    """
    Инициализация БД Постгрес
    """
    try:
        conn = await asyncpg.connect(settings.PG_URL)
        return conn
    except Exception:
        return False


class Pg:

    @staticmethod
    async def add_result(result: ResultAnalyzer) -> bool:
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
