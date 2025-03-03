import time

from ai_handler import ai_generate_answer
import gradio as gr
from config import settings
from common import generate_filename
import threading


# Функция для приветствия, загрузки изображения, сохранения и вывода текста
def greet_and_upload(image):
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

    filename = generate_filename(8) + '.jpg'
    # Сохраняем изображение в формате JPEG
    save_path = f"./images/{filename}"
    image.save(save_path, "JPEG")

    pass
    # Шаг 2: Анализ изображения с помощью OpenAI
    time.sleep(0.5)
    image_description = ai_generate_answer(f'{settings.API_URL}/{filename}')
    # Возвращаем сообщение о загрузке, которое сразу обновится
    return image_description


def gradio_main():
    # Создаем блоки с компонентами
    with gr.Blocks() as iface:
        # Приветствие
        gr.Markdown("### Привет! Загрузи изображение, и я покажу его описание и сохраню.")

        # Ввод изображения
        image_input = gr.Image(type="pil", label="Загрузите изображение")

        # Вывод сообщения о загрузке и анализа изображения
        final_message_output = gr.Textbox(label="Результат", interactive=False)

        # Соединяем компоненты с функцией
        image_input.change(fn=greet_and_upload, inputs=image_input, outputs=final_message_output, show_progress='minimal')

    # Запускаем интерфейс
    iface.launch(max_file_size='6mb', server_name='0.0.0.0', server_port=7861)
