@echo off
echo Проверка зарегистрированных пользователей...
echo.

echo Все пользователи:
python manage.py list_users
echo.

echo Только админы:
python manage.py list_users --admin-only
echo.

pause
