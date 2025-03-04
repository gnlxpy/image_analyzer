import asyncio
from idlelib.window import add_windows_to_menu

from ai_handler import ai_generate_answer
import gradio as gr
from config import settings
from common import generate_filename
from sql_handler import Pg, ResultAnalyzer
from sql_handler import init_pg, close_pg


pool = None


# Функция для приветствия, загрузки изображения, сохранения и вывода текста
async def upload_and_analyze(image):

    yield "### 💾 Загружаем изображение..."

    # Проверка размера изображения и уменьшение, если необходимо
    max_size = 1000
    width, height = image.size
    if width > max_size or height > max_size:
        if width > height:
            new_width = max_size
            new_height = int((max_size / width) * height)
        else:
            new_height = max_size
            new_width = int((max_size / height) * width)

        image = image.resize((new_width, new_height))

    # генерируем имя файла
    filename = generate_filename(8) + '.jpg'
    # Сохраняем изображение в формате JPEG
    save_path = f"./images/{filename}"
    image.save(save_path, "JPEG")

    # Шаг 2: Анализ изображения с помощью OpenAI
    await asyncio.sleep(1)
    yield "### 🤖 Анализируем изображение..."

    image_url = f'{settings.API_URL}/{filename}'
    image_description = await ai_generate_answer(image_url)

    # добавляем результат в БД
    await Pg.add_result(ResultAnalyzer(
        image_url=image_url,
        description=image_description
    ))

    image_description += f'\n{image_url}'

    # Возвращаем сообщение о загрузке, которое сразу обновится
    yield image_description


async def gradio_main():
    await init_pg()
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
    await close_pg()
