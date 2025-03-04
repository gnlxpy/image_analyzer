from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Query, HTTPException, status as fastapi_status
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

app = FastAPI()
app.mount('/images', StaticFiles(directory='images'), name='images')


@app.get("/images/{file}")
async def get_image(file: str):
    files = os.listdir('./images')
    if file in files:
        return FileResponse(f"./images/{file}", media_type="image/jpg")
    else:
        raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND, detail='id задачи не найден')


async def fastapi_main():
    print('FASTAPI STARTED!')
    config = uvicorn.Config("fastapi_handler:app", host='0.0.0.0', port=8000)
    server = uvicorn.Server(config)
    await server.serve()
