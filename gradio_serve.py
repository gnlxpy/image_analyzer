import asyncio
from ai_handler import ai_generate_answer
import gradio as gr
from config import settings
from common import generate_filename, set_width_height
from sql_handler import Pg, ResultAnalyzer


async def upload_and_analyze(image, max_size: int = 1000):
    """
    Основная функция ресайза, сохранения, анализа фотографии
    :param max_size: максимальный размер по большей стороне
    :param image: объект изображения
    :return: генерация текстов
    """
    yield "### 💾 Загружаем изображение..."

    # Проверка размера изображения и уменьшение, если необходимо
    width, height = image.size
    resize, new_width, new_height = set_width_height(width, height, max_size)
    if resize:
        image = image.resize((new_width, new_height))

    # генерируем имя файла
    filename = generate_filename(8) + '.jpg'
    # Сохраняем изображение в формате JPEG
    image.save(f"./images/{filename}", "JPEG")
    await asyncio.sleep(1)

    # Шаг 2: Анализ изображения с помощью OpenAI
    yield "### 🤖 Анализируем изображение..."

    image_url = f'{settings.API_URL}/{filename}'
    image_description = await ai_generate_answer(image_url)
    if image_description:
        # добавляем результат в БД
        await Pg.add_result(ResultAnalyzer(
            image_url=image_url,
            description=image_description
        ))

        # Возвращаем сообщение с описанием
        yield image_description + f'\n{image_url}'
    else:
        yield "### 😢 К сожалению произошла ошибка"


async def gradio_main():
    """
    Основная функция создания интерфейса
    """
    # Создаем блоки с компонентами
    with gr.Blocks() as iface:
        # Приветствие
        gr.Markdown("### Привет! Загрузи изображение, и я покажу его описание и сохраню 🪄✨")

        # Ввод изображения
        image_input = gr.Image(type="pil", label="Загрузите изображение")

        # Вывод сообщения о загрузке и анализа изображения
        final_message_output = gr.Markdown("### Здесь будет результат 💫")

        # Соединяем компоненты с функцией
        image_input.change(fn=upload_and_analyze, inputs=image_input, outputs=final_message_output, show_progress='minimal')

    # Запускаем интерфейс
    print('GRADIO STARTED!')
    iface.launch(max_file_size='10mb', server_name='0.0.0.0', server_port=7861)
