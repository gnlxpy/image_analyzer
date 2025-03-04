import random
import string
import threading


def generate_filename(length: int) -> str:
    """
    Генерация имени файла
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def run_threaded(target, *args, **kwargs):
    """
    Запуск функции в отельном потоке
    """
    thread = threading.Thread(target=target, args=args, kwargs=kwargs, daemon=True).start()
    return thread


def set_width_height(width, height, max_size):
    """
    Проверка и изменение размеров в зависимости от максимального
    :param width: ширина
    :param height: высота
    :param max_size: максимальное занчение
    :return: статус, измененная ширина, измененная высота
    """
    if width > max_size or height > max_size:
        if width > height:
            new_width = max_size
            new_height = int((max_size / width) * height)
        else:
            new_height = max_size
            new_width = int((max_size / height) * width)
        return True, new_width, new_height
    else:
        return False, None, None
