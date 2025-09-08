@echo off
echo Создание админа...
echo.

echo 1. Создание миграций...
python manage.py makemigrations
echo.

echo 2. Применение миграций...
python manage.py migrate
echo.

echo 3. Создание админа...
python manage.py create_admin --email "kok321416xxx@yandex.ru" --password "Superego1939" --username "Superego1939"
echo.

echo 4. Запуск сервера...
echo Админка будет доступна по адресу: http://localhost:8000/admin/
echo.
python manage.py runserver
