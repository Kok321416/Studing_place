from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = "Создает группы пользователей (Модераторы, Пользователи)"

    def handle(self, *args, **options):
        """Создает группы пользователей"""
        groups_to_create = ["Модераторы", "Пользователи"]

        created_count = 0
        existing_count = 0

        for group_name in groups_to_create:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Создана группа: {group_name}")
                )
            else:
                existing_count += 1
                self.stdout.write(
                    self.style.WARNING(f"⚠️  Группа уже существует: {group_name}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\n📊 Результат:"
                f"\n   Создано новых групп: {created_count}"
                f"\n   Уже существовало: {existing_count}"
                f"\n   Всего групп: {Group.objects.count()}"
            )
        )

        # Показываем все существующие группы
        self.stdout.write(self.style.SUCCESS("\n📋 Все группы в системе:"))
        for group in Group.objects.all():
            self.stdout.write(f"   - {group.name}")

        self.stdout.write(
            self.style.SUCCESS(
                "\n💡 Совет: Назначайте пользователей в группы через админ-панель"
                "\n   /admin/auth/group/"
            )
        )
