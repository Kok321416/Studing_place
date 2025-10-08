from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Показывает всех зарегистрированных пользователей"

    def add_arguments(self, parser):
        parser.add_argument(
            "--admin-only",
            action="store_true",
            help="Показать только суперпользователей",
        )

    def handle(self, *args, **options):
        admin_only = options["admin_only"]

        if admin_only:
            users = User.objects.filter(is_superuser=True)
            self.stdout.write(self.style.SUCCESS("🔐 СУПЕРПОЛЬЗОВАТЕЛИ (АДМИНЫ):"))
        else:
            users = User.objects.all()
            self.stdout.write(self.style.SUCCESS("👥 ВСЕ ПОЛЬЗОВАТЕЛИ:"))

        if not users.exists():
            self.stdout.write(self.style.WARNING("❌ Пользователи не найдены!"))
            return

        self.stdout.write("=" * 80)

        for i, user in enumerate(users, 1):
            # Определяем статус пользователя
            status_icons = []
            if user.is_superuser:
                status_icons.append("🔐")
            if user.is_staff:
                status_icons.append("👨‍💼")
            if user.is_active:
                status_icons.append("✅")
            else:
                status_icons.append("❌")

            status = " ".join(status_icons)

            self.stdout.write(f"{i}. {user.username} ({user.email})")
            self.stdout.write(f"   Статус: {status}")
            self.stdout.write(f"   Имя: {user.first_name} {user.last_name}")
            self.stdout.write(
                f'   Дата регистрации: {user.date_joined.strftime("%d.%m.%Y %H:%M")}'
            )
            self.stdout.write(
                f'   Последний вход: {user.last_login.strftime("%d.%m.%Y %H:%M") if user.last_login else "Никогда"}'
            )

            # Показываем права доступа
            permissions = []
            if user.is_superuser:
                permissions.append("Суперпользователь")
            if user.is_staff:
                permissions.append("Персонал")
            if user.is_active:
                permissions.append("Активный")

            self.stdout.write(f'   Права: {", ".join(permissions)}')
            self.stdout.write("-" * 80)

        # Статистика
        total_users = User.objects.count()
        superusers = User.objects.filter(is_superuser=True).count()
        staff_users = User.objects.filter(is_staff=True).count()
        active_users = User.objects.filter(is_active=True).count()

        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("📊 СТАТИСТИКА:")
        self.stdout.write("=" * 80)
        self.stdout.write(f"Всего пользователей: {total_users}")
        self.stdout.write(f"Суперпользователей: {superusers}")
        self.stdout.write(f"Персонала: {staff_users}")
        self.stdout.write(f"Активных: {active_users}")

        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("🌐 ПОЛЕЗНЫЕ ССЫЛКИ:")
        self.stdout.write("=" * 80)
        self.stdout.write("Админка: http://localhost:8000/admin/")
        self.stdout.write("API пользователей: http://localhost:8000/api/users/")
        self.stdout.write("API токенов: http://localhost:8000/api/token/")

        if superusers > 0:
            self.stdout.write("\n" + "=" * 80)
            self.stdout.write("🔑 ДАННЫЕ ДЛЯ ВХОДА В АДМИНКУ:")
            self.stdout.write("=" * 80)
            for user in User.objects.filter(is_superuser=True):
                self.stdout.write(f"Email: {user.email}")
                self.stdout.write(f"Username: {user.username}")
                self.stdout.write("Пароль: [скрыт]")
                self.stdout.write("-" * 40)
