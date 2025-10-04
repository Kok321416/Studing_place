from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson
from decimal import Decimal
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Создает тестовые курсы с уроками'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=3,
            help='Количество тестовых курсов для создания'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # Создаем тестового пользователя если его нет
        test_user, created = User.objects.get_or_create(
            email='test@example.com',
            defaults={
                'username': 'testuser',
                'first_name': 'Тестовый',
                'last_name': 'Пользователь',
                'is_active': True
            }
        )
        
        if created:
            test_user.set_password('testpass123')
            test_user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Создан тестовый пользователь: {test_user.email}')
            )
        
        # Тестовые курсы
        test_courses = [
            {
                'title': 'Python для начинающих',
                'description': 'Полный курс по изучению Python с нуля. Изучите основы программирования, работу с данными, создание веб-приложений и многое другое.',
                'price': Decimal('2999.00'),
                'lessons': [
                    {
                        'title': 'Введение в Python',
                        'description': 'Знакомство с языком Python, установка и настройка среды разработки.',
                        'video_link': 'https://www.youtube.com/watch?v=kqtD5dpn9C8'
                    },
                    {
                        'title': 'Переменные и типы данных',
                        'description': 'Изучение основных типов данных в Python: числа, строки, списки, словари.',
                        'video_link': 'https://www.youtube.com/watch?v=8DvywoWv6fI'
                    },
                    {
                        'title': 'Условные операторы и циклы',
                        'description': 'Работа с условными операторами if/else и циклами for/while.',
                        'video_link': 'https://www.youtube.com/watch?v=OnDr4J2UXSA'
                    },
                    {
                        'title': 'Функции и модули',
                        'description': 'Создание и использование функций, работа с модулями и пакетами.',
                        'video_link': 'https://www.youtube.com/watch?v=9Os0o3wzS_I'
                    }
                ]
            },
            {
                'title': 'Django Web Development',
                'description': 'Создание веб-приложений с помощью Django. Изучите модели, представления, шаблоны, аутентификацию и развертывание.',
                'price': Decimal('4999.00'),
                'lessons': [
                    {
                        'title': 'Введение в Django',
                        'description': 'Установка Django, создание первого проекта и приложения.',
                        'video_link': 'https://www.youtube.com/watch?v=F5mRW0jo-U4'
                    },
                    {
                        'title': 'Модели и база данных',
                        'description': 'Создание моделей Django, работа с ORM и миграциями.',
                        'video_link': 'https://www.youtube.com/watch?v=1R6v2QqYS1E'
                    },
                    {
                        'title': 'Представления и URL-маршруты',
                        'description': 'Создание представлений, настройка URL-маршрутов и обработка запросов.',
                        'video_link': 'https://www.youtube.com/watch?v=0oZC0VQo-1s'
                    },
                    {
                        'title': 'Шаблоны и статические файлы',
                        'description': 'Создание HTML-шаблонов, работа с контекстом и статическими файлами.',
                        'video_link': 'https://www.youtube.com/watch?v=3Xc_9BZPDWs'
                    },
                    {
                        'title': 'Аутентификация и авторизация',
                        'description': 'Система пользователей, регистрация, вход и права доступа.',
                        'video_link': 'https://www.youtube.com/watch?v=UmljXZIypDc'
                    }
                ]
            },
            {
                'title': 'JavaScript и React',
                'description': 'Современная разработка фронтенда с JavaScript и React. Изучите ES6+, компоненты, хуки, состояние и маршрутизацию.',
                'price': Decimal('3999.00'),
                'lessons': [
                    {
                        'title': 'Основы JavaScript ES6+',
                        'description': 'Современный JavaScript: стрелочные функции, деструктуризация, модули.',
                        'video_link': 'https://www.youtube.com/watch?v=hdI2bqOjy3c'
                    },
                    {
                        'title': 'Введение в React',
                        'description': 'Создание первого React-приложения, компоненты и JSX.',
                        'video_link': 'https://www.youtube.com/watch?v=w7ejDZ8SWv8'
                    },
                    {
                        'title': 'Состояние и хуки',
                        'description': 'useState, useEffect и другие хуки React.',
                        'video_link': 'https://www.youtube.com/watch?v=TNhaISOUy6Q'
                    },
                    {
                        'title': 'Маршрутизация в React',
                        'description': 'React Router для создания SPA-приложений.',
                        'video_link': 'https://www.youtube.com/watch?v=59IXY5IDrBA'
                    }
                ]
            },
            {
                'title': 'Бесплатный курс: HTML и CSS',
                'description': 'Основы веб-разработки. Изучите HTML для структуры и CSS для стилизации веб-страниц.',
                'price': None,  # Бесплатный курс
                'lessons': [
                    {
                        'title': 'Введение в HTML',
                        'description': 'Основы HTML, теги, атрибуты и структура документа.',
                        'video_link': 'https://www.youtube.com/watch?v=qz0aGYrrlhU'
                    },
                    {
                        'title': 'Основы CSS',
                        'description': 'Селекторы, свойства, стилизация текста и блоков.',
                        'video_link': 'https://www.youtube.com/watch?v=1Rs2ND1ryYc'
                    },
                    {
                        'title': 'Flexbox и Grid',
                        'description': 'Современные методы верстки с Flexbox и CSS Grid.',
                        'video_link': 'https://www.youtube.com/watch?v=JJSoEo8JSnc'
                    }
                ]
            },
            {
                'title': 'Базы данных и SQL',
                'description': 'Работа с реляционными базами данных. Изучите SQL, проектирование БД, оптимизацию запросов.',
                'price': Decimal('2499.00'),
                'lessons': [
                    {
                        'title': 'Введение в базы данных',
                        'description': 'Основы реляционных БД, нормализация, ключи.',
                        'video_link': 'https://www.youtube.com/watch?v=HXV3zeQKqGY'
                    },
                    {
                        'title': 'Основы SQL',
                        'description': 'SELECT, INSERT, UPDATE, DELETE, JOIN.',
                        'video_link': 'https://www.youtube.com/watch?v=7S_tz1z_5bA'
                    },
                    {
                        'title': 'Продвинутый SQL',
                        'description': 'Подзапросы, индексы, транзакции, хранимые процедуры.',
                        'video_link': 'https://www.youtube.com/watch?v=5OdVJbNCSso'
                    }
                ]
            }
        ]
        
        created_courses = 0
        
        for i, course_data in enumerate(test_courses[:count]):
            # Проверяем, существует ли уже такой курс
            if Course.objects.filter(title=course_data['title']).exists():
                self.stdout.write(
                    self.style.WARNING(f'Курс "{course_data["title"]}" уже существует, пропускаем')
                )
                continue
            
            # Создаем курс
            course = Course.objects.create(
                title=course_data['title'],
                description=course_data['description'],
                price=course_data['price'],
                owner=test_user
            )
            
            # Создаем уроки для курса
            for j, lesson_data in enumerate(course_data['lessons']):
                Lesson.objects.create(
                    title=lesson_data['title'],
                    description=lesson_data['description'],
                    video_link=lesson_data['video_link'],
                    course=course,
                    owner=test_user
                )
            
            created_courses += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'Создан курс "{course.title}" с {len(course_data["lessons"])} уроками'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно создано {created_courses} тестовых курсов!'
            )
        )
        
        # Показываем информацию о созданных курсах
        self.stdout.write('\n' + '='*50)
        self.stdout.write('СОЗДАННЫЕ КУРСЫ:')
        self.stdout.write('='*50)
        
        for course in Course.objects.filter(owner=test_user).order_by('-created_at'):
            price_info = f"{course.price} ₽" if course.price else "БЕСПЛАТНО"
            lessons_count = course.lessons.count()
            self.stdout.write(f'• {course.title} - {price_info} ({lessons_count} уроков)')
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write('ИНФОРМАЦИЯ ДЛЯ ТЕСТИРОВАНИЯ:')
        self.stdout.write('='*50)
        self.stdout.write(f'Тестовый пользователь: {test_user.email}')
        self.stdout.write(f'Пароль: testpass123')
        self.stdout.write(f'Всего курсов в системе: {Course.objects.count()}')
        self.stdout.write(f'Всего уроков в системе: {Lesson.objects.count()}')
        self.stdout.write('\nДля просмотра курсов с оплатой перейдите по адресу:')
        self.stdout.write('http://localhost:8000/courses-with-payment/')
