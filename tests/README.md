# Тесты проекта

Этот каталог содержит все тестовые файлы проекта.

## Структура тестов

- `test_all_endpoints.py` - Комплексные тесты всех API эндпоинтов
- `test_crud_and_subscriptions.py` - Тесты CRUD операций и подписок
- `test_validators.py` - Тесты валидаторов (YouTube ссылки)
- `test_courses_models.py` - Тесты моделей курсов
- `test_users_models.py` - Тесты моделей пользователей

## Запуск тестов

### Обычный запуск тестов
```bash
python manage.py test tests
```

### Запуск конкретного тестового файла
```bash
python manage.py test tests.test_all_endpoints
python manage.py test tests.test_crud_and_subscriptions
python manage.py test tests.test_validators
```

### Запуск с покрытием кода

#### Windows (bat файл)
```bash
run_tests_with_coverage.bat
```

#### Python скрипт
```bash
python run_tests_with_coverage.py
```

#### Ручной запуск
```bash
# Установка coverage
pip install coverage

# Запуск тестов с покрытием
coverage run --source=. manage.py test tests

# Генерация HTML отчета
coverage html

# Просмотр краткого отчета
coverage report
```

## Просмотр отчета о покрытии

После запуска тестов с покрытием HTML отчет будет создан в директории `htmlcov/`. 
Откройте файл `htmlcov/index.html` в браузере для просмотра детального отчета.

## Конфигурация coverage

Настройки coverage находятся в файле `.coveragerc` в корне проекта.

## Исключения из покрытия

Следующие файлы и директории исключены из анализа покрытия:
- Миграции Django (`*/migrations/*`)
- Виртуальные окружения (`*/venv/*`, `*/env/*`)
- Тестовые файлы (`*/tests/*`)
- Статические файлы (`*/static/*`)
- Шаблоны (`*/templates/*`)
- Файлы конфигурации
