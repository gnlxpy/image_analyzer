from openai import AsyncOpenAI
from config import settings


async def ai_generate_answer(image_url: str) -> str | bool:
    """
    Функция для генерации ответа с использованием GPT-4
    """
    try:
        # инициализация ИИ
        client = AsyncOpenAI(api_key=settings.OPENAI_TOKEN)

        # подготовка сообщений для выгрузки
        messages = [
            {
                'role': 'system',
                'content': settings.OPENAI_SYSTEM
            },
            {
                "role": "user", "content": [
                {"type": "text", "text": "Опиши, что изображено на этом изображении?"},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]}
        ]

        # отправка запроса
        response = await client.chat.completions.create(
            messages=messages,
            model="gpt-4o-mini",
            max_tokens=3000,
        )

        # Получаем и возвращаем ответ
        answer = response.choices[0].message.content
        return answer
    except Exception:
        return False
