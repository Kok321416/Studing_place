# 🐘 Настройка PostgreSQL для Django LMS

## 📋 Требования

- Установленный PostgreSQL
- Python 3.8+
- pip

## 🚀 Установка PostgreSQL

### Windows:
1. Скачайте PostgreSQL с официального сайта: https://www.postgresql.org/download/windows/
2. Установите с паролем для пользователя `postgres`
3. Запомните пароль!

### macOS:
```bash
brew install postgresql
brew services start postgresql
```

### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

## 🔧 Настройка базы данных

### 1. Подключение к PostgreSQL:
```bash
# Windows (если добавлен в PATH)
psql -U postgres

# macOS/Linux
sudo -u postgres psql
```

### 2. Создание базы данных:
```sql
CREATE DATABASE django_lms;
CREATE USER django_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE django_lms TO django_user;
\q
```

### 3. Создание .env файла:
Скопируйте `env_sample.txt` в `.env` и заполните параметры:

```bash
# Windows
copy env_sample.txt .env

# macOS/Linux
cp env_sample.txt .env
```

### 4. Редактирование .env:
```env
# Database Settings
DB_NAME=django_lms
DB_USER=django_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
```

## 📦 Установка зависимостей

```bash
pip install -r requirements.txt
```

## 🗄️ Применение миграций

```bash
python manage.py makemigrations
python manage.py migrate
```

## 🧪 Тестирование подключения

```bash
python manage.py runserver
```

Если нет ошибок - PostgreSQL настроен правильно!

## 🚨 Возможные проблемы

### Ошибка "connection refused":
- Проверьте, что PostgreSQL запущен
- Проверьте порт (по умолчанию 5432)

### Ошибка "authentication failed":
- Проверьте пароль в .env
- Проверьте права пользователя

### Ошибка "database does not exist":
- Создайте базу данных
- Проверьте имя в .env

## 🔒 Безопасность

- Используйте сложные пароли
- Не коммитьте .env файл в Git
- Ограничьте доступ к базе данных только с localhost

## 📚 Полезные команды PostgreSQL

```sql
-- Список баз данных
\l

-- Список пользователей
\du

-- Подключение к базе
\c django_lms

-- Список таблиц
\dt

-- Выход
\q
```
