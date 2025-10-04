from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Создает суперпользователя для админки'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            default='admin@example.com',
            help='Email админ пользователя'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='admin123',
            help='Пароль админ пользователя'
        )
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Имя пользователя'
        )

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        username = options['username']
        
        # Проверяем, существует ли уже пользователь
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'Пользователь с email {email} уже существует!')
            )
            return
        
        # Создаем суперпользователя
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name='Админ',
            last_name='Пользователь'
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Создан суперпользователь!')
        )
        self.stdout.write(f'📧 Email: {email}')
        self.stdout.write(f'👤 Username: {username}')
        self.stdout.write(f'🔑 Пароль: {password}')
        self.stdout.write(f'🌐 Админка: http://localhost:8000/admin/')
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write('ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ:')
        self.stdout.write('='*50)
        self.stdout.write('1. Запустите сервер: python manage.py runserver')
        self.stdout.write('2. Откройте админку: http://localhost:8000/admin/')
        self.stdout.write('3. Войдите с данными выше')
        self.stdout.write('4. Создайте курс в разделе "Courses"')
        self.stdout.write('5. Добавьте уроки прямо в курсе (inline формы)')
        self.stdout.write('6. Вставьте YouTube ссылки в поле "Video link"')
