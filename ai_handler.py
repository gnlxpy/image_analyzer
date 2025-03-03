from openai import OpenAI
from config import settings


def ai_generate_answer(image_url: str) -> str:
    """
    Функция для генерации ответа с использованием GPT-4
    """
    # инициализация ИИ
    client = OpenAI(api_key=settings.OPENAI_TOKEN)
    messages = [
        {
            'role': 'system',
            'content': 'You analyze the uploaded image in detail and point by point as an experienced designer. First you talk about the general, and then you describe the style, colors, and details of the image in more detail. If a geographic location is depicted, you try to explain where it is. At the end you say what this image might be useful for.'
        },
        {
            "role": "user", "content": [
            {"type": "text", "text": "Опиши, что изображено на этом изображении?"},
            {"type": "image_url", "image_url": {"url": image_url}}
        ]}
    ]

    # отправляем запрос
    response = client.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",
        max_tokens=1000,
    )

    # Получаем и возвращаем ответ
    answer = response.choices[0].message.content

    return answer
