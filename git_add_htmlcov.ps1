# Скрипт для добавления htmlcov/ в git репозиторий

Write-Host "Удаление htmlcov/ из .gitignore..." -ForegroundColor Yellow
$content = Get-Content .gitignore
$filteredContent = $content | Where-Object { $_ -notmatch 'htmlcov/' }
$filteredContent | Set-Content .gitignore

Write-Host "Удаление htmlcov/ из git кэша..." -ForegroundColor Yellow
git rm -r --cached htmlcov/ 2>$null

Write-Host "Добавление всех файлов..." -ForegroundColor Yellow
git add .

Write-Host "Коммит изменений..." -ForegroundColor Yellow
git commit -m "Add htmlcov directory with coverage reports"

Write-Host "Push изменений..." -ForegroundColor Yellow
git push

Write-Host "Готово! htmlcov/ добавлен в репозиторий." -ForegroundColor Green
