# 🎓 Django LMS Project

Проект системы управления обучением (LMS) на Django с Django REST Framework.

## 📋 Описание проекта

Этот проект реализует базовую систему управления курсами и уроками с кастомной моделью пользователя, использующей email для авторизации.

## ✨ Функциональность

### 🔐 Пользователи
- Кастомная модель пользователя с авторизацией по email
- Дополнительные поля: телефон, город, аватарка
- Полная интеграция с Django Admin

### 📚 Курсы
- Создание, редактирование, удаление курсов
- Загрузка превью-изображений
- Полное API через ViewSet

### 📖 Уроки
- Создание, редактирование, удаление уроков
- Связь с курсами (один курс - много уроков)
- Загрузка превью и ссылки на видео
- API через Generic-классы

## 🚀 Установка и запуск

### 1. Клонирование репозитория
```bash
git clone <your-repo-url>
cd Studing_place
```

### 2. Создание виртуального окружения
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# или
source .venv/bin/activate  # Linux/Mac
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Применение миграций
```bash
python manage.py migrate
```

### 5. Создание суперпользователя
```bash
python manage.py createsuperuser
```

### 6. Запуск сервера
```bash
python manage.py runserver
```

## 🌐 Доступные URL-адреса

- **Админка Django:** http://127.0.0.1:8000/admin/
- **API курсов:** http://127.0.0.1:8000/api/courses/
- **API уроков:** http://127.0.0.1:8000/api/lessons/

## 🧪 Тестирование API

### Курсы (ViewSet)
- **GET** `/api/courses/` - список курсов
- **POST** `/api/courses/` - создание курса
- **GET** `/api/courses/{id}/` - получение курса
- **PUT** `/api/courses/{id}/` - обновление курса
- **DELETE** `/api/courses/{id}/` - удаление курса

### Уроки (Generic-классы)
- **GET** `/api/lessons/` - список уроков
- **POST** `/api/lessons/` - создание урока
- **GET** `/api/lessons/{id}/` - получение урока
- **PUT** `/api/lessons/{id}/` - обновление урока
- **DELETE** `/api/lessons/{id}/` - удаление урока

## 📁 Структура проекта

```
Studing_place/
├── config/                 # Основные настройки проекта
│   ├── settings.py        # Настройки Django и DRF
│   └── urls.py           # Главные URL-маршруты
├── users/                 # Приложение пользователей
│   ├── models.py         # Кастомная модель User
│   └── admin.py          # Админка для пользователей
├── courses/               # Приложение курсов и уроков
│   ├── models.py         # Модели Course и Lesson
│   ├── views.py          # Views для API
│   ├── serializers.py    # Сериализаторы
│   ├── urls.py           # URL-маршруты API
│   └── admin.py          # Админка для курсов и уроков
├── media/                 # Загруженные файлы (не в Git)
│   ├── avatars/          # Аватары пользователей
│   ├── course_previews/  # Превью курсов
│   └── lesson_previews/  # Превью уроков
├── .gitignore            # Исключения для Git
├── requirements.txt       # Зависимости проекта
├── README.md             # Документация
└── manage.py             # Управление Django
```

## 🔧 Технологии

- **Django 5.2.3** - веб-фреймворк
- **Django REST Framework 3.16.1** - API фреймворк
- **Pillow** - работа с изображениями
- **SQLite** - база данных (для разработки)

## 📝 Примеры использования

### Создание курса
```json
POST /api/courses/
{
    "title": "Python для начинающих",
    "description": "Базовый курс по Python",
    "preview": "[файл изображения]"
}
```

### Создание урока
```json
POST /api/lessons/
{
    "title": "Введение в Python",
    "description": "Первое знакомство с языком",
    "preview": "[файл изображения]",
    "video_link": "https://youtube.com/watch?v=example",
    "course": 1
}
```

## 🚨 Важные замечания

- Папка `media/` не отслеживается Git (добавлена в .gitignore)
- Для продакшена рекомендуется использовать PostgreSQL
- Настройте CORS если планируете фронтенд на отдельном домене
- Добавьте аутентификацию и права доступа для продакшена

## 📄 Лицензия

MIT License

## 👨‍💻 Автор

Создано в рамках обучения Django и DRF
