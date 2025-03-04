import asyncio

from fastapi_handler import fastapi_main
from common import run_threaded
from gradio_handler import gradio_main


if __name__ == '__main__':
    run_threaded(fastapi_main)
    asyncio.run(gradio_main())
