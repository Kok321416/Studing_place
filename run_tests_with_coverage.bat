@echo off
echo Запуск тестов с покрытием...

REM Установка coverage если не установлен
pip install coverage

REM Запуск тестов с coverage
coverage run --source=. manage.py test tests

REM Генерация HTML отчета
echo Генерация HTML отчета...
coverage html

REM Показать краткий отчет
echo.
echo Краткий отчет о покрытии:
coverage report

echo.
echo HTML отчет создан в директории htmlcov/
echo Откройте htmlcov/index.html в браузере для просмотра детального отчета
pause
