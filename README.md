# Образовательная платформа Django

Современная образовательная платформа, построенная на Django 4.2.7 и Django REST Framework с JWT аутентификацией.

## 🚀 Реализованные функции

### ✅ Задание 1: JWT аутентификация и CRUD для пользователей

- **JWT аутентификация**: Настроена с использованием `djangorestframework-simplejwt`
- **CRUD для пользователей**: Полный набор операций для управления пользователями
- **Регистрация**: Эндпоинт `/api/users/register/` доступен для неавторизованных пользователей
- **Защита эндпоинтов**: Все API эндпоинты защищены аутентификацией, кроме регистрации и получения токенов

#### Эндпоинты аутентификации:
- `POST /api/token/` - получение JWT токена
- `POST /api/token/refresh/` - обновление JWT токена
- `POST /api/users/register/` - регистрация пользователя
- `GET/PUT /api/users/profile/` - профиль пользователя
- `GET /api/users/list/` - список пользователей

### ✅ Задание 2: Система модераторов

- **Группа модераторов**: Создана с соответствующими разрешениями
- **Права модераторов**: Могут просматривать и редактировать любые курсы/уроки, но не создавать/удалять
- **Кастомные разрешения**: Реализованы в `courses/permissions.py`
- **Автоматическое создание групп**: Кастомная команда `python manage.py create_groups`

#### Разрешения для модераторов:
- `view_course` - просмотр курсов
- `change_course` - редактирование курсов
- `view_lesson` - просмотр уроков
- `change_lesson` - редактирование уроков

### ✅ Задание 3: Объектно-уровневые разрешения

- **Поле владельца**: Добавлено поле `owner` в модели `Course` и `Lesson`
- **Автоматическое назначение**: При создании объекта автоматически назначается владелец
- **Фильтрация по владельцу**: Пользователи видят только свои объекты (если не модераторы)
- **Метод `perform_create`**: Автоматически связывает создаваемый объект с авторизованным пользователем

#### Права доступа:
- **Модераторы**: Полный доступ ко всем объектам
- **Обычные пользователи**: Доступ только к своим объектам
- **Создание**: Автоматическое назначение владельца

## 🎨 HTML интерфейс

### Фиолетовый дизайн
- **Цветовая схема**: Градиентный фиолетовый фон (#667eea → #764ba2)
- **Современный UI**: Bootstrap 5 + Font Awesome иконки
- **Адаптивность**: Полностью адаптивный дизайн для всех устройств

### Интересные кнопки
- **Анимации**: Hover эффекты, трансформации, тени
- **Градиенты**: Красивые градиентные кнопки с анимацией
- **Интерактивность**: Анимации появления элементов, hover эффекты

### Навигация
- **Главная страница**: `/` - приветствие и обзор возможностей
- **Курсы**: `/courses/html/courses/` - список всех курсов
- **Уроки**: `/lessons/html/lessons/` - список всех уроков
- **API**: `/api/` - доступ к REST API
- **Админка**: `/admin/` - управление через Django Admin

## 🛠 Техническая реализация

### Модели данных
```python
# Пользователь (кастомная модель)
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/')

# Курс
class Course(models.Model):
    title = models.CharField(max_length=200)
    preview = models.ImageField(upload_to='course_previews/')
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

# Урок
class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    preview = models.ImageField(upload_to='lesson_previews/')
    video_link = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
```

### Система разрешений
```python
class IsModeratorOrOwnerForModify(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.groups.filter(name='Модераторы').exists():
            return True
        return obj.owner == request.user
```

### API Views
- **CourseViewSet**: Полный CRUD для курсов с динамическими разрешениями
- **LessonListCreateView**: Создание и просмотр уроков
- **LessonDetailView**: Детальный просмотр, редактирование и удаление уроков
- **UserRegistrationView**: Регистрация пользователей
- **UserProfileView**: Управление профилем пользователя

## 📦 Установка и запуск

### Требования
- Python 3.8+
- Django 4.2.7
- PostgreSQL (рекомендуется) или SQLite

### Установка зависимостей
```bash
pip install -r requirements.txt
```

### Настройка базы данных
```bash
python manage.py makemigrations
python manage.py migrate
```

### Создание групп и суперпользователя
```bash
python manage.py create_groups
python manage.py createsuperuser
```

### Запуск сервера
```bash
python manage.py runserver
```

## 🔐 Безопасность

- **JWT токены**: Безопасная аутентификация
- **Объектно-уровневые разрешения**: Защита на уровне объектов
- **Групповые разрешения**: Ролевая модель доступа
- **Валидация данных**: Проверка входных данных
- **CSRF защита**: Встроенная защита от CSRF атак

## 📱 API эндпоинты

### Курсы
- `GET /api/courses/` - список курсов
- `POST /api/courses/` - создание курса
- `GET /api/courses/{id}/` - детали курса
- `PUT /api/courses/{id}/` - обновление курса
- `DELETE /api/courses/{id}/` - удаление курса

### Уроки
- `GET /api/lessons/` - список уроков
- `POST /api/lessons/` - создание урока
- `GET /api/lessons/{id}/` - детали урока
- `PUT /api/lessons/{id}/` - обновление урока
- `DELETE /api/lessons/{id}/` - удаление урока

### Пользователи
- `POST /api/users/register/` - регистрация
- `GET/PUT /api/users/profile/` - профиль
- `GET /api/users/list/` - список пользователей

## 🎯 Особенности реализации

- **Автоматическое назначение владельца**: При создании объекта
- **Динамические разрешения**: В зависимости от действия и роли пользователя
- **Фильтрация данных**: Пользователи видят только свои объекты
- **Кастомная команда**: Автоматическое создание групп и разрешений
- **Фикстуры**: Готовые данные для групп пользователей
- **Медиа файлы**: Поддержка загрузки изображений для курсов и уроков

## 🚀 Дальнейшее развитие

- Добавление системы платежей
- Интеграция с внешними образовательными платформами
- Система уведомлений
- Аналитика и отчеты
- Мобильное приложение
- Система комментариев и отзывов

## 📄 Лицензия

Проект создан в образовательных целях.
