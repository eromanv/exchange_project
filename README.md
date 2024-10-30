# Django Exchange Rate API

## Описание
Этот проект представляет собой Django API, который предоставляет текущий курс доллара к рублю и сохраняет 10 последних запросов курса. Эндпоинт `/get-current-usd/` обновляет курс не чаще чем раз в 10 секунд и сохраняет данные в базе.

## Стек технологий
- Python 3
- Django 4.2
- Django REST Framework
- SQLite (выбран для небольшой локальной разработки)

## Установка и запуск

1. **Клонирование репозитория:**
   ```bash
   git clone https://github.com/your-username/exchange_project.git
   cd exchange_project

2. **Установка виртуального окружения и зависимостей**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  
    # для Windows используйте `venv\Scripts\activate`
    pip install -r requirements.txt

3. **Применение миграций:**

    ```bash
    python manage.py migrate

4. **Запуск сервера:**

    ```bash
    python manage.py runserver

5. **Проверка работы API:**
    Откройте браузер или используйте curl/Postman, чтобы обратиться по адресу:

    ```sql
    http://127.0.0.1:8000/get-current-usd/

6. **Тестирование**
    Запуск тестов:

    ```bash
    python manage.py test

7. **Структура проекта**
    * exchange/: основное приложение Django.
    * get_current_usd/: эндпоинт для получения курса доллара.
    * ExchangeRate: модель для хранения курса и времени его получения.

8. **Эндпоинты**
    * /get-current-usd/: Возвращает текущий курс доллара к рублю и 10 последних запросов.
    * /admin/: Админка существует, но в целом - она особо и не нужна.
