#!/usr/bin/env python3
"""
Скрипт для проверки работоспособности проекта Django
"""

import os
import sys
import django
from pathlib import Path

# Добавляем путь к проекту в PYTHONPATH
project_path = Path(__file__).parent
sys.path.insert(0, str(project_path))

# Устанавливаем переменную окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

def check_project():
    """Проверяет работоспособность проекта"""
    print("🔍 Проверка проекта Django...")
    print("=" * 50)
    
    try:
        # Инициализируем Django
        django.setup()
        print("✅ Django инициализирован успешно")
        
        # Проверяем импорт моделей
        from courses.models import Course, Lesson
        print("✅ Модели курсов импортированы")
        
        from users.models import User, Payment
        print("✅ Модели пользователей импортированы")
        
        # Проверяем импорт сериализаторов
        from courses.serializers import CourseSerializer, LessonSerializer
        print("✅ Сериализаторы курсов импортированы")
        
        from users.serializers import PaymentSerializer
        print("✅ Сериализаторы пользователей импортированы")
        
        # Проверяем импорт views
        from courses.views import CourseViewSet, LessonListCreateView, LessonDetailView
        print("✅ Views курсов импортированы")
        
        from users.views import PaymentViewSet
        print("✅ Views пользователей импортированы")
        
        # Проверяем импорт фильтров
        from users.filters import PaymentFilter
        print("✅ Фильтры импортированы")
        
        # Проверяем настройки Django
        from django.conf import settings
        print(f"✅ Настройки Django загружены (DEBUG: {settings.DEBUG})")
        
        # Проверяем приложения
        print(f"✅ Установленные приложения: {len(settings.INSTALLED_APPS)}")
        
        # Проверяем базу данных
        from django.db import connection
        if connection.ensure_connection():
            print("✅ Подключение к базе данных успешно")
        else:
            print("⚠️  Проблемы с подключением к базе данных")
        
        print("\n🎉 Проект готов к работе!")
        print("=" * 50)
        print("📋 Что можно сделать дальше:")
        print("1. Создать суперпользователя: python manage.py createsuperuser")
        print("2. Запустить сервер: python manage.py runserver")
        print("3. Открыть админку: http://127.0.0.1:8000/admin/")
        print("4. API курсов: http://127.0.0.1:8000/api/courses/")
        print("5. API пользователей: http://127.0.0.1:8000/api/users/")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print(f"📍 Тип ошибки: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = check_project()
    sys.exit(0 if success else 1)
