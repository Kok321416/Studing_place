# Studing Place - Django REST API

## Описание проекта
Проект представляет собой API для образовательной платформы с курсами, уроками и системой платежей.

## Выполненные задания

### ✅ Задание 1: Поле количества уроков в сериализаторе курса
- Добавлено поле `lessons_count` в `CourseSerializer` с использованием `SerializerMethodField()`
- Поле автоматически подсчитывает количество уроков для каждого курса

### ✅ Задание 2: Модель Платежи
- Создана модель `Payment` в приложении `users`
- Поля: пользователь, дата оплаты, курс/урок, сумма, способ оплаты
- Добавлена валидация (курс и урок не могут быть заполнены одновременно)
- Создана миграция для новой модели

### ✅ Задание 3: Поле уроков в сериализаторе курса
- Добавлено поле `lessons` в `CourseSerializer`
- Выводит полную информацию о всех уроках курса
- Один сериализатор выдает и количество уроков, и информацию по всем урокам

### ✅ Задание 4: Фильтрация для API платежей
- Настроена фильтрация по курсу, уроку и способу оплаты
- Добавлена возможность сортировки по дате оплаты
- Создан API эндпоинт `/api/users/payments/`

## Установка и запуск

1. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Примените миграции:**
   ```bash
   python manage.py migrate
   ```

3. **Создайте суперпользователя:**
   ```bash
   python manage.py createsuperuser
   ```

4. **Запустите сервер:**
   ```bash
   python manage.py runserver
   ```

## Создание тестовых данных

### Вариант 1: Фикстура
```bash
python manage.py loaddata payments
```

### Вариант 2: Кастомная команда
```bash
python manage.py create_payments
```

## API Endpoints

### Курсы
- `GET /api/courses/` - список курсов с количеством уроков и информацией об уроках

### Платежи
- `GET /api/users/payments/` - список платежей
- `GET /api/users/payments/?course=1` - фильтрация по курсу
- `GET /api/users/payments/?lesson=1` - фильтрация по уроку
- `GET /api/users/payments/?payment_method=transfer` - фильтрация по способу оплаты
- `GET /api/users/payments/?ordering=payment_date` - сортировка по дате (по возрастанию)
- `GET /api/users/payments/?ordering=-payment_date` - сортировка по дате (по убыванию)

## Структура проекта

```
Studing_place/
├── config/                 # Основные настройки Django
├── courses/               # Приложение курсов
│   ├── models.py         # Модели Course и Lesson
│   ├── serializers.py    # Сериализаторы с полями lessons_count и lessons
│   └── views.py          # API представления
├── users/                 # Приложение пользователей
│   ├── models.py         # Модели User и Payment
│   ├── serializers.py    # Сериализатор Payment
│   ├── filters.py        # Фильтры для Payment
│   ├── views.py          # PaymentViewSet
│   ├── admin.py          # Админка для Payment
│   └── management/       # Кастомные команды
└── requirements.txt       # Зависимости проекта
```

## Технологии

- Django 4.2.7
- Django REST Framework 3.14.0
- Django Filter 23.5
- Pillow 10.1.0
- Python 3.13
