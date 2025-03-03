from common import run_threaded
from gradio_handler import gradio_main
from storage_handler import fastapi_main


if __name__ == '__main__':
    run_threaded(fastapi_main)
    gradio_main()
