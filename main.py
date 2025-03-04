import asyncio
from fastapi_serve import fastapi_main
from common import run_threaded
from gradio_serve import gradio_main


if __name__ == '__main__':
    # запуск 2 отдельных потоков FastAPI и Gradio
    run_threaded(fastapi_main)
    asyncio.run(gradio_main())
