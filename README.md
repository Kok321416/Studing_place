# Studing Place - Django REST API

## Описание проекта
Современная образовательная платформа с красивым интерфейсом в фиолетовых тонах, предоставляющая REST API для работы с курсами, уроками и пользователями. Проект включает систему аутентификации JWT, права доступа, фильтрацию и возможность деплоя на удаленный сервер.

## ✨ Особенности

- 🎨 **Красивый интерфейс** в фиолетовых тонах с анимациями
- 🔐 **JWT аутентификация** с системой разрешений
- 👥 **Система групп** (Модераторы и Пользователи)
- 🛡️ **Объектные права доступа** (пользователи видят только свои данные)
- 📱 **Адаптивный дизайн** для всех устройств
- 🐳 **Docker поддержка** для легкого деплоя
- 🚀 **GitHub Actions CI/CD** для автоматического деплоя
- 🗄️ **PostgreSQL** для надежного хранения данных

## 🚀 Быстрый старт

### Локальная разработка

1. **Клонируйте репозиторий:**
   ```bash
   git clone <your-repo-url>
   cd Studing_place
   ```

2. **Создайте виртуальное окружение:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate  # Windows
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройте переменные окружения:**
   ```bash
   cp env_sample.txt .env
   # Отредактируйте .env файл с вашими настройками
   ```

5. **Настройте базу данных PostgreSQL:**
   - Создайте базу данных `django_lms`
   - Укажите данные в `.env` файле

6. **Примените миграции:**
   ```bash
   python manage.py migrate
   ```

7. **Создайте суперпользователя:**
   ```bash
   python manage.py createsuperuser
   ```

8. **Создайте группы пользователей:**
   ```bash
   python manage.py create_groups
   ```

9. **Запустите сервер:**
   ```bash
   python manage.py runserver
   ```

### Docker (Рекомендуется для production)

1. **Скопируйте и настройте .env файл:**
   ```bash
   cp env_sample.txt .env
   ```

2. **Запустите с Docker Compose:**
   ```bash
   docker-compose up -d
   ```

3. **Создайте суперпользователя:**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

4. **Создайте группы:**
   ```bash
   docker-compose exec web python manage.py create_groups
   ```

## 🌐 Доступ к приложению

- **Главная страница:** http://localhost:8000/
- **API:** http://localhost:8000/api/
- **Админка:** http://localhost:8000/admin/
- **Курсы:** http://localhost:8000/courses/html/
- **Уроки:** http://localhost:8000/lessons/html/

## 📚 API Endpoints

### Аутентификация
- `POST /api/token/` - получение JWT токена
- `POST /api/token/refresh/` - обновление токена

### Пользователи
- `POST /api/users/register/` - регистрация нового пользователя
- `GET /api/users/profile/` - профиль текущего пользователя
- `PUT /api/users/profile/` - обновление профиля
- `GET /api/users/list/` - список пользователей (для модераторов)

### Курсы
- `GET /api/courses/` - список курсов
- `POST /api/courses/` - создание курса (только авторизованные)
- `GET /api/courses/{id}/` - детали курса
- `PUT /api/courses/{id}/` - обновление курса (владелец или модератор)
- `DELETE /api/courses/{id}/` - удаление курса (владелец или модератор)

### Уроки
- `GET /api/lessons/` - список уроков
- `POST /api/lessons/` - создание урока (только авторизованные)
- `GET /api/lessons/{id}/` - детали урока
- `PUT /api/lessons/{id}/` - обновление урока (владелец или модератор)
- `DELETE /api/lessons/{id}/` - удаление урока (владелец или модератор)

## 🔧 Настройка удаленного сервера

### Требования к серверу
- Ubuntu 20.04/22.04
- Docker и Docker Compose
- Git
- SSH доступ

### Пошаговая настройка

1. **Подключитесь к серверу:**
   ```bash
   ssh user@your-server-ip
   ```

2. **Установите Docker:**
   ```bash
   sudo apt update
   sudo apt install docker.io docker-compose git
   sudo usermod -aG docker $USER
   ```

3. **Клонируйте репозиторий:**
   ```bash
   git clone <your-repo-url> /var/www/studing_place
   cd /var/www/studing_place
   ```

4. **Настройте переменные окружения:**
   ```bash
   cp env_sample.txt .env
   nano .env  # Настройте параметры
   ```

5. **Запустите приложение:**
   ```bash
   docker-compose up -d
   ```

6. **Настройте Nginx (опционально):**
   ```bash
   sudo apt install nginx
   # Настройте конфигурацию nginx
   ```

## 🔐 GitHub Secrets

Для автоматического деплоя настройте следующие секреты в GitHub:

- `SERVER_HOST` - IP адрес вашего сервера
- `SERVER_USER` - пользователь для SSH подключения
- `SSH_PRIVATE_KEY` - приватный SSH ключ
- `DB_PASSWORD` - пароль для PostgreSQL

## 🏗️ GitHub Actions

Проект настроен для автоматического деплоя:

1. **При каждом push в main/develop** запускаются тесты
2. **После успешных тестов** происходит автоматический деплой
3. **Docker образы** собираются и развертываются на сервере

## 🎨 Дизайн

Интерфейс выполнен в фиолетовых тонах с:
- Градиентными фонами
- Плавными анимациями
- Стеклянными эффектами
- Адаптивной версткой
- Минималистичным дизайном

## 📁 Структура проекта

```
Studing_place/
├── .github/workflows/     # GitHub Actions
├── config/                # Основные настройки Django
├── courses/               # Приложение курсов
├── users/                 # Приложение пользователей
├── templates/             # HTML шаблоны
├── static/               # Статические файлы
├── docker-compose.yml    # Docker конфигурация
├── Dockerfile            # Docker образ
├── nginx.conf            # Nginx конфигурация
└── env_sample.txt        # Шаблон переменных окружения
```

## 🛠️ Технологии

- **Backend:** Django 4.2.7, Django REST Framework 3.16.1
- **Database:** PostgreSQL 13
- **Authentication:** JWT (djangorestframework-simplejwt)
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
- **Deployment:** Docker, Docker Compose, Nginx
- **CI/CD:** GitHub Actions
- **Python:** 3.11+

## 📝 Лицензия

MIT License

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature ветку
3. Внесите изменения
4. Создайте Pull Request

## 📞 Поддержка

Если у вас есть вопросы или предложения, создайте Issue в репозитории.
