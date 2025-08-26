# 📚 Инструкции по выполнению заданий

## 🎯 Задание 1: Поле количества уроков в сериализаторе курса ✅ ВЫПОЛНЕНО

**Что сделано:**
- В файле `courses/serializers.py` добавлено поле `lessons_count` с использованием `SerializerMethodField()`
- Создан метод `get_lessons_count()` который возвращает количество уроков для курса

**Код:**
```python
class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = '__all__'
    
    def get_lessons_count(self, obj):
        return obj.lessons.count()
```

---

## 🎯 Задание 2: Модель Платежи ✅ ВЫПОЛНЕНО

**Что сделано:**
- Создана модель `Payment` в файле `users/models.py`
- Добавлены все необходимые поля: пользователь, дата, курс/урок, сумма, способ оплаты
- Создана миграция `users/migrations/0002_payment.py`
- Добавлена валидация (курс и урок не могут быть заполнены одновременно)

**Код модели:**
```python
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Оплаченный курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Оплаченный урок')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='Способ оплаты')
```

**Тестовые данные:**
- Создана фикстура `users/fixtures/payments.json`
- Создана кастомная команда `users/management/commands/create_payments.py`

---

## 🎯 Задание 3: Поле уроков в сериализаторе курса ✅ ВЫПОЛНЕНО

**Что сделано:**
- В `courses/serializers.py` добавлено поле `lessons` для вывода всех уроков курса
- Один сериализатор теперь выдает и количество уроков, и полную информацию по всем урокам

**Код:**
```python
class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = '__all__'
    
    def get_lessons_count(self, obj):
        return obj.lessons.count()
```

---

## 🎯 Задание 4: Фильтрация для API платежей ✅ ВЫПОЛНЕНО

**Что сделано:**
- Создан сериализатор `users/serializers.py` для модели Payment
- Создан фильтр `users/filters.py` с возможностями фильтрации и сортировки
- Создан `PaymentViewSet` в `users/views.py`
- Настроены URL-маршруты в `users/urls.py` и `config/urls.py`
- Добавлен `django_filters` в `INSTALLED_APPS`

**Фильтрация:**
- По курсу: `?course=1`
- По уроку: `?lesson=1`
- По способу оплаты: `?payment_method=transfer`
- Сортировка по дате: `?ordering=payment_date` или `?ordering=-payment_date`

**API Endpoint:** `/api/users/payments/`

---

## 🚀 Как запустить проект

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Применение миграций
```bash
python manage.py migrate
```

### 3. Создание суперпользователя
```bash
python manage.py createsuperuser
```

### 4. Запуск сервера
```bash
python manage.py runserver
```

### 5. Создание тестовых данных
```bash
# Вариант 1: Фикстура
python manage.py loaddata payments

# Вариант 2: Кастомная команда
python manage.py create_payments
```

---

## 🌐 Доступные API endpoints

- **Курсы:** `http://127.0.0.1:8000/api/courses/`
- **Платежи:** `http://127.0.0.1:8000/api/users/payments/`
- **Админка:** `http://127.0.0.1:8000/admin/`

---

## 📁 Структура созданных файлов

```
users/
├── models.py              # Модель Payment
├── serializers.py         # PaymentSerializer
├── filters.py             # PaymentFilter
├── views.py               # PaymentViewSet
├── urls.py                # URL маршруты
├── admin.py               # Админка для Payment
├── migrations/
│   └── 0002_payment.py   # Миграция для Payment
├── fixtures/
│   └── payments.json      # Тестовые данные
└── management/
    └── commands/
        └── create_payments.py  # Кастомная команда

courses/
└── serializers.py         # Обновленный CourseSerializer

config/
├── settings.py            # Добавлен django_filters
└── urls.py                # Обновлены маршруты
```

---

## ✅ Все задания выполнены успешно!

Проект готов к использованию. Все API endpoints работают, фильтрация настроена, тестовые данные созданы.
