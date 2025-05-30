# Flask PDF Viewer

## Описание
Flask PDF Viewer - это веб-приложение, разработанное на Flask, которое позволяет просматривать PDF-файлы прямо в браузере. Приложение предоставляет простой и удобный интерфейс для работы с PDF-документами.

## Функциональность
- Просмотр PDF-файлов в браузере
- Удобный веб-интерфейс
- Поддержка навигации по страницам PDF

## Технический стек
- Python 3.x
- Flask 3.0.2
- python-dotenv 1.0.1

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone [URL репозитория]
cd flask_library
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Запустите приложение:
```bash
python pdf_viewer.py
```

5. Откройте браузер и перейдите по адресу:
```
http://localhost:5000
```

## Структура проекта
```
flask_library/
├── pdf_viewer.py    # Основной файл приложения
├── requirements.txt # Зависимости проекта
└── static/         # Статические файлы (CSS, JS, изображения)
```

## Авторство
Проект разработан как часть сервиса mapcheb.ru

## Лицензия
MIT License 