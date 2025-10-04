# 💳 Настройка системы оплаты и тестирование

## 🎨 Визуальное отображение кнопки оплаты

### ✅ Реализованные улучшения:

1. **Современный дизайн кнопок оплаты:**
   - Закругленные кнопки с градиентным фоном
   - Четкие контуры и тени
   - Анимации при наведении
   - Адаптивный дизайн для мобильных устройств

2. **Интуитивный интерфейс:**
   - Кнопка "Оплатить курс" для платных курсов
   - Кнопка "Начать обучение" для бесплатных курсов
   - Отображение цены в отдельном блоке
   - Статус оплаты (оплачено/ожидает)

3. **Удобная навигация:**
   - Добавлена ссылка "Курсы с оплатой" в главное меню
   - Быстрый доступ к API документации
   - Информация о курсе и уроках

## 🚀 Как добавить тестовые курсы

### Вариант 1: Через Django команду (рекомендуется)

```bash
# Активируйте виртуальное окружение
.venv\Scripts\Activate.ps1

# Создайте тестовые курсы
python manage.py create_test_courses

# Создайте 5 курсов (по умолчанию 3)
python manage.py create_test_courses --count 5
```

### Вариант 2: Через Django Admin

1. Перейдите в админку: `http://localhost:8000/admin/`
2. Войдите как суперпользователь
3. Перейдите в раздел "Courses" → "Courses"
4. Нажмите "Add Course"
5. Заполните поля:
   - **Title**: Название курса
   - **Description**: Описание курса
   - **Price**: Цена (оставьте пустым для бесплатного курса)
   - **Owner**: Выберите пользователя

### Вариант 3: Через API

```bash
# Получите токен авторизации
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'

# Создайте курс
curl -X POST http://localhost:8000/api/courses/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title": "Мой тестовый курс",
    "description": "Описание курса",
    "price": "1999.00"
  }'
```

## 🎯 Тестовые данные

После выполнения команды `create_test_courses` будут созданы:

### 📚 Курсы:
1. **Python для начинающих** - 2,999 ₽ (4 урока)
2. **Django Web Development** - 4,999 ₽ (5 уроков)
3. **JavaScript и React** - 3,999 ₽ (4 урока)
4. **Бесплатный курс: HTML и CSS** - БЕСПЛАТНО (3 урока)
5. **Базы данных и SQL** - 2,499 ₽ (3 урока)

### 👤 Тестовый пользователь:
- **Email**: test@example.com
- **Пароль**: testpass123
- **Права**: Обычный пользователь

## 🔧 Настройка Stripe

### 1. Получите ключи Stripe:
1. Зарегистрируйтесь на [Stripe Dashboard](https://dashboard.stripe.com/register)
2. Перейдите в раздел "Developers" → "API keys"
3. Скопируйте ключи:
   - **Publishable key** (начинается с `pk_test_`)
   - **Secret key** (начинается с `sk_test_`)

### 2. Добавьте ключи в .env файл:
```env
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
STRIPE_SECRET_KEY=sk_test_your_secret_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
```

### 3. Тестовые карты Stripe:
```
Успешная оплата: 4242 4242 4242 4242
Отклоненная карта: 4000 0000 0000 0002
Требует 3D Secure: 4000 0025 0000 3155
```

## 🌐 Доступные страницы

### Основные страницы:
- **Главная**: `http://localhost:8000/`
- **Курсы (API)**: `http://localhost:8000/courses/`
- **Курсы с оплатой**: `http://localhost:8000/courses-with-payment/`
- **Уроки**: `http://localhost:8000/lessons/`
- **Пользователи**: `http://localhost:8000/users/`
- **Админка**: `http://localhost:8000/admin/`

### API документация:
- **Swagger UI**: `http://localhost:8000/swagger/`
- **ReDoc**: `http://localhost:8000/redoc/`

### API эндпоинты:
- **Курсы**: `http://localhost:8000/api/courses/`
- **Платежи**: `http://localhost:8000/api/users/payments/`
- **Пользователи**: `http://localhost:8000/api/users/`

## 🧪 Тестирование оплаты

### 1. Создайте тестовые курсы:
```bash
python manage.py create_test_courses
```

### 2. Запустите сервер:
```bash
python manage.py runserver
```

### 3. Откройте страницу с курсами:
```
http://localhost:8000/courses-with-payment/
```

### 4. Протестируйте оплату:
1. Нажмите "Оплатить курс" на любом платном курсе
2. Введите тестовые данные карты: `4242 4242 4242 4242`
3. Заполните любые данные (дата, CVC, имя)
4. Нажмите "Pay" в Stripe Checkout

### 5. Проверьте результат:
- **Успешная оплата**: Перенаправление на `/payment/success/`
- **Отмена оплаты**: Перенаправление на `/payment/cancel/`

## 🔍 Отладка

### Проверка логов:
```bash
# Запустите сервер с отладкой
python manage.py runserver --verbosity=2
```

### Проверка базы данных:
```bash
# Войдите в Django shell
python manage.py shell

# Проверьте курсы
from courses.models import Course
Course.objects.all()

# Проверьте платежи
from users.models import Payment
Payment.objects.all()
```

### Проверка Stripe:
1. Откройте [Stripe Dashboard](https://dashboard.stripe.com/test/payments)
2. Проверьте раздел "Payments" для просмотра тестовых платежей

## 🎉 Готово!

Теперь у вас есть:
- ✅ Современный интерфейс с кнопками оплаты
- ✅ Тестовые курсы для демонстрации
- ✅ Полная интеграция со Stripe
- ✅ API документация
- ✅ Система управления платежами

Наслаждайтесь тестированием! 🚀
