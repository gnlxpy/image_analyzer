# Image Analyzer

## Описание
Тестовый проект на интерфейсе Gradio для распознавания изображений с помощью openai.

## Структура проекта
```
image_analyzer/
|-- images/                # файлы сохраненных изображений
|-- ai_handler.py          # работа с API openai через AsyncOpenAI
|-- common.py              # вспомогательные функции
|-- config.py              # загрузка конфигов через pydantic_settings
|-- fastapi_serve.py       # запуск сервиса RESTful FastAPI
|-- gradio_server.py       # веб-интерфейс Gradio
|-- main.py                # основной код запуска потоков
|-- sql_handler.py         # обработчик запросов в Postgresql через asyncpg
```

# Файл с конфигом
Необходим файл .env со следующими переменными (используется pydantic_settings для работы с переменными окружения):
```
OPENAI_SYSTEM='You analyze the uploaded image in detail and point by point as an experienced designer. First you talk about the general, and then you describe the style, colors, and details of the image in more detail. If a geographic location is depicted, you try to explain where it is. At the end you say what this image might be useful for.'
OPENAI_TOKEN='{{Токен openai}}'
HOST='{{Адрес данного сервера}}'
PG_USER='{{Postgresql login}}'
PG_PSW='{{Postgresql password}}'
PG_HOST='{{Postgresql ip}}'
```

* OPENAI_SYSTEM - указан стандартный промт в текущей версии приложения
* PG_USER, PG_PSW, PG_HOST - могут не указываться, функционал бд не будет применяться