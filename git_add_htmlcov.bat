@echo off
echo Удаление htmlcov/ из .gitignore...
powershell -Command "(Get-Content .gitignore) | Where-Object { $_ -notmatch 'htmlcov/' } | Set-Content .gitignore"

echo Удаление htmlcov/ из git кэша...
git rm -r --cached htmlcov/ 2>nul

echo Добавление всех файлов...
git add .

echo Коммит изменений...
git commit -m "Add htmlcov directory with coverage reports"

echo Push изменений...
git push

echo Готово! htmlcov/ добавлен в репозиторий.
pause
