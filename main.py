import asyncio
from gradio_handler import gradio_main
from fastapi_handler import fastapi_main


async def main():
    await asyncio.gather(fastapi_main(), gradio_main())


if __name__ == '__main__':
    asyncio.run(main())
