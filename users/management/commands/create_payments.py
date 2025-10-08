from django.core.management.base import BaseCommand
from users.models import User, Payment
from courses.models import Course, Lesson
from decimal import Decimal


class Command(BaseCommand):
    help = "Создает тестовые платежи"

    def handle(self, *args, **options):
        try:
            # Получаем первого пользователя
            user = User.objects.first()
            if not user:
                self.stdout.write(
                    self.style.ERROR(
                        "Пользователи не найдены. Сначала создайте пользователя."
                    )
                )
                return

            # Получаем первый курс
            course = Course.objects.first()
            if not course:
                self.stdout.write(
                    self.style.ERROR("Курсы не найдены. Сначала создайте курс.")
                )
                return

            # Получаем первый урок
            lesson = Lesson.objects.first()
            if not lesson:
                self.stdout.write(
                    self.style.ERROR("Уроки не найдены. Сначала создайте урок.")
                )
                return

            # Удаляем существующие платежи
            Payment.objects.all().delete()

            # Создаем тестовые платежи
            Payment.objects.create(
                user=user,
                course=course,
                lesson=None,
                amount=Decimal("15000.00"),
                payment_method="transfer",
            )

            Payment.objects.create(
                user=user,
                course=None,
                lesson=lesson,
                amount=Decimal("2000.00"),
                payment_method="cash",
            )

            Payment.objects.create(
                user=user,
                course=course,
                lesson=None,
                amount=Decimal("12000.00"),
                payment_method="transfer",
            )

            self.stdout.write(self.style.SUCCESS("Тестовые платежи успешно созданы!"))
            self.stdout.write(f"Создано платежей: {Payment.objects.count()}")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка при создании платежей: {e}"))
