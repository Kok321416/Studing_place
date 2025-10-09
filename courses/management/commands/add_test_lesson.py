from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson

User = get_user_model()


class Command(BaseCommand):
    help = "Добавляет тестовый урок с YouTube ссылкой"

    def add_arguments(self, parser):
        parser.add_argument(
            "--title", type=str, default="Тестовый урок", help="Название урока"
        )
        parser.add_argument(
            "--description",
            type=str,
            default="Описание тестового урока",
            help="Описание урока",
        )
        parser.add_argument(
            "--video-url",
            type=str,
            default="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            help="YouTube ссылка на видео",
        )
        parser.add_argument(
            "--course-id",
            type=int,
            help="ID курса (если не указан, будет использован первый доступный)",
        )

    def handle(self, *args, **options):
        title = options["title"]
        description = options["description"]
        video_url = options["video_url"]
        course_id = options["course_id"]

        # Получаем курс
        if course_id:
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Курс с ID {course_id} не найден"))
                return
        else:
            course = Course.objects.first()
            if not course:
                self.stdout.write(
                    self.style.ERROR("Нет доступных курсов. Сначала создайте курс.")
                )
                return

        # Получаем пользователя
        user = User.objects.first()
        if not user:
            self.stdout.write(
                self.style.ERROR(
                    "Нет пользователей в системе. Сначала создайте пользователя."
                )
            )
            return

        # Создаем урок
        lesson = Lesson.objects.create(
            title=title,
            description=description,
            video_link=video_url,
            course=course,
            owner=user,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Создан урок "{lesson.title}" в курсе "{course.title}"'
            )
        )

        self.stdout.write(f"📺 YouTube ссылка: {lesson.video_link}")
        self.stdout.write(f"👤 Владелец: {lesson.owner.email}")
        self.stdout.write(f"📚 Курс: {lesson.course.title}")

        # Показываем информацию о курсе
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("ИНФОРМАЦИЯ О КУРСЕ:")
        self.stdout.write("=" * 50)
        self.stdout.write(f"Название: {course.title}")
        self.stdout.write(f"Описание: {course.description}")
        self.stdout.write(f"Цена: {course.price} ₽" if course.price else "Бесплатно")
        self.stdout.write(f"Количество уроков: {course.lessons.count()}")

        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("ВСЕ УРОКИ В КУРСЕ:")
        self.stdout.write("=" * 50)
        for i, lesson in enumerate(course.lessons.all(), 1):
            self.stdout.write(f"{i}. {lesson.title}")
            self.stdout.write(f"   📺 {lesson.video_link}")

        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("ПОЛЕЗНЫЕ ССЫЛКИ:")
        self.stdout.write("=" * 50)
        self.stdout.write(f"API курса: http://localhost:8000/api/courses/{course.id}/")
        self.stdout.write(f"API урока: http://localhost:8000/api/lessons/{lesson.id}/")
        self.stdout.write("Админка: http://localhost:8000/admin/")
        self.stdout.write(
            "Курсы с оплатой: http://localhost:8000/courses-with-payment/"
        )
