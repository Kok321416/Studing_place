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

## 🚀 Деплой и CI/CD

### GitHub Actions Workflow

Проект настроен для автоматического тестирования и деплоя через GitHub Actions.

#### Файл `.github/workflows/deploy.yml`:
- **Автоматические тесты**: Запускаются при каждом push в репозиторий
- **PostgreSQL**: Используется для тестирования
- **Деплой**: Автоматически разворачивается на сервере после успешных тестов
- **Docker**: Полная контейнеризация приложения

### Docker развертывание

#### Dockerfile
- **Многоэтапная сборка**: Оптимизация размера образа
- **Безопасность**: Отдельный пользователь для Django
- **Production-ready**: Gunicorn для production сервера

#### docker-compose.yml
- **PostgreSQL**: База данных в контейнере
- **Nginx**: Веб-сервер для статических файлов
- **Django**: Приложение в контейнере
- **Volumes**: Персистентное хранение данных

### Настройка сервера

#### 1. Подготовка сервера
```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker и Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Установка Git
sudo apt install git -y
```

#### 2. Клонирование проекта
```bash
git clone https://github.com/your-username/Studing_place.git
cd Studing_place
```

#### 3. Настройка переменных окружения
```bash
# Скопировать шаблон
cp env_sample.txt .env

# Отредактировать .env файл
nano .env
```

#### 4. Запуск приложения
```bash
# Запуск через Docker Compose
docker-compose up -d

# Проверка статуса
docker-compose ps

# Просмотр логов
docker-compose logs -f
```

### GitHub Secrets

Для автоматического деплоя необходимо настроить следующие секреты в GitHub:

#### Обязательные секреты:
- `SERVER_HOST` - IP адрес вашего сервера
- `SERVER_USER` - имя пользователя SSH (обычно `ubuntu` или `root`)
- `SSH_PRIVATE_KEY` - приватный SSH ключ для доступа к серверу
- `DB_PASSWORD` - пароль для PostgreSQL

#### Как добавить секреты:
1. Перейдите в Settings → Secrets and variables → Actions
2. Нажмите "New repository secret"
3. Добавьте каждый секрет с соответствующим именем

### Nginx конфигурация

Файл `nginx.conf` настроен для:
- **Проксирование**: Запросы к Django приложению
- **Статические файлы**: Раздача CSS, JS, изображений
- **Медиа файлы**: Раздача загруженных пользователями файлов
- **Лимиты**: Максимальный размер загружаемых файлов

### Безопасность

#### Настройки безопасности:
- **SSH ключи**: Обязательный доступ по SSH ключам
- **Firewall**: Закрыты ненужные порты
- **Docker**: Изолированные контейнеры
- **Non-root**: Приложение запускается от пользователя django

#### Рекомендации:
```bash
# Настройка файрвола
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# Отключение root логина
sudo nano /etc/ssh/sshd_config
# Установить PermitRootLogin no
sudo systemctl restart ssh
```

### Мониторинг

#### Проверка работы:
```bash
# Статус контейнеров
docker-compose ps

# Логи приложения
docker-compose logs web

# Логи базы данных
docker-compose logs db

# Логи Nginx
docker-compose logs nginx
```

#### Перезапуск приложения:
```bash
# Перезапуск всех сервисов
docker-compose restart

# Перезапуск только Django
docker-compose restart web

# Обновление и перезапуск
docker-compose pull
docker-compose up -d
```

### Troubleshooting

#### Частые проблемы:
1. **Порт занят**: Проверьте `docker-compose ps`
2. **Ошибки миграций**: `docker-compose exec web python manage.py migrate`
3. **Статические файлы**: `docker-compose exec web python manage.py collectstatic`
4. **Права доступа**: Проверьте владельца файлов

#### Полезные команды:
```bash
# Подключение к контейнеру
docker-compose exec web bash

# Выполнение команд Django
docker-compose exec web python manage.py shell

# Просмотр переменных окружения
docker-compose exec web env
```

## 📄 Лицензия

Проект создан в образовательных целях.
