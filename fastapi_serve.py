from fastapi import FastAPI, HTTPException, status as fastapi_status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

# инициализация АПИ
app = FastAPI()
# монтирование папки с изображениями
app.mount('/images', StaticFiles(directory='images'), name='images')


@app.get("/")
def read_root():
    return {"Images Host status": True}


@app.get("/images/{file}")
async def get_image(file: str):
    """
    Функция проверки наличия и выдачи изображений
    :param file: имя файла
    :return: файл | 404
    """
    files = os.listdir('./images')
    if file in files:
        return FileResponse(f"./images/{file}", media_type="image/jpg")
    else:
        raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND, detail='id задачи не найден')


def fastapi_main():
    print('FASTAPI STARTED!')
    uvicorn.run("fastapi_serve:app", host='0.0.0.0', port=8000)
