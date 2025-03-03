from fastapi import FastAPI, Request, Query, HTTPException, status as fastapi_status
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os


app = FastAPI()
app.mount('/images', StaticFiles(directory='images'), name='images')


@app.get("/images/{file}")
async def get_image(file: str):
    print(file)
    files = os.listdir('./images')
    print(files)
    if file in files:
        return FileResponse(f"./images/{file}", media_type="image/jpg")
    else:
        raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND, detail='id задачи не найден')


if __name__ == '__main__':
    uvicorn.run("storage_handler:app", reload=True, use_colors=True, workers=4, host='0.0.0.0', port=8000)
