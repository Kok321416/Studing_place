from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from courses.models import Course, Lesson

class Command(BaseCommand):
    help = 'Создает группы модераторов и пользователей с соответствующими разрешениями'

    def handle(self, *args, **options):
        # Создаем группу модераторов
        moderators_group, created = Group.objects.get_or_create(name='Модераторы')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модераторы" создана'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Модераторы" уже существует'))

        # Создаем группу обычных пользователей
        users_group, created = Group.objects.get_or_create(name='Пользователи')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Пользователи" создана'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Пользователи" уже существует'))

        # Получаем content types для моделей
        course_ct = ContentType.objects.get_for_model(Course)
        lesson_ct = ContentType.objects.get_for_model(Lesson)

        # Разрешения для модераторов (просмотр и редактирование, но не создание/удаление)
        moderator_permissions = [
            Permission.objects.get(content_type=course_ct, codename='view_course'),
            Permission.objects.get(content_type=course_ct, codename='change_course'),
            Permission.objects.get(content_type=lesson_ct, codename='view_lesson'),
            Permission.objects.get(content_type=lesson_ct, codename='change_lesson'),
        ]

        # Разрешения для обычных пользователей (только просмотр)
        user_permissions = [
            Permission.objects.get(content_type=course_ct, codename='view_course'),
            Permission.objects.get(content_type=lesson_ct, codename='view_lesson'),
        ]

        # Назначаем разрешения группам
        moderators_group.permissions.set(moderator_permissions)
        users_group.permissions.set(user_permissions)

        self.stdout.write(self.style.SUCCESS('Разрешения успешно назначены группам'))
        
        # Выводим информацию о созданных группах
        self.stdout.write('\nСозданные группы:')
        self.stdout.write(f'- Модераторы: {moderators_group.permissions.count()} разрешений')
        self.stdout.write(f'- Пользователи: {users_group.permissions.count()} разрешений')
