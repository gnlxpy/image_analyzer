from common import run_threaded
import gradio_handler
import storage_handler


if __name__ == '__main__':
    run_threaded(storage_handler)
    run_threaded(gradio_handler)
