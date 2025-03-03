import random
import string
import threading


def generate_filename(length: int) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def run_threaded(func, *args, **kwargs):
    threading.Thread(target=func, args=args, kwargs=kwargs).start()
