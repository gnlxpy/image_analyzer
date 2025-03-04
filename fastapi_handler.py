from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Query, HTTPException, status as fastapi_status
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from sql_handler import init_pg, close_pg

# Глобальная переменная для пула соединений
pool = None


app = FastAPI()
app.mount('/images', StaticFiles(directory='images'), name='images')


@asynccontextmanager
async def lifespan(_: FastAPI):
    global pool
    pool = await init_pg()
    yield
    await close_pg()


@app.get("/images/{file}")
async def get_image(file: str):
    files = os.listdir('./images')
    if file in files:
        return FileResponse(f"./images/{file}", media_type="image/jpg")
    else:
        raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND, detail='id задачи не найден')


def fastapi_main():
    print('FASTAPI STARTED!')
    uvicorn.run("fastapi_handler:app", host='0.0.0.0', port=8000)
