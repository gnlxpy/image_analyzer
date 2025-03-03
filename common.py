import random
import string
import threading


def generate_filename(length: int) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def run_threaded(target, *args, **kwargs):
    thread = threading.Thread(target=target, args=args, kwargs=kwargs)
    thread.start()
    return thread
