Write-Host "Создание админа..." -ForegroundColor Green
Write-Host ""

Write-Host "1. Создание миграций..." -ForegroundColor Yellow
python manage.py makemigrations
Write-Host ""

Write-Host "2. Применение миграций..." -ForegroundColor Yellow
python manage.py migrate
Write-Host ""

Write-Host "3. Создание админа..." -ForegroundColor Yellow
python manage.py create_admin --email "kok321416xxx@yandex.ru" --password "Superego1939" --username "Superego1939"
Write-Host ""

Write-Host "4. Запуск сервера..." -ForegroundColor Yellow
Write-Host "Админка будет доступна по адресу: http://localhost:8000/admin/" -ForegroundColor Cyan
Write-Host ""
python manage.py runserver
