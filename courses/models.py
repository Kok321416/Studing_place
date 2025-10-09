from django.db import models
from django.conf import settings
from django.utils import timezone


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="course_previews/",
        verbose_name="Превью курса",
        null=True,
        blank=True,
    )
    description = models.TextField(verbose_name="Описание курса")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена курса",
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание урока")
    preview = models.ImageField(
        upload_to="lesson_previews/",
        verbose_name="Превью",
        null=True,
        blank=True,
    )
    video_link = models.URLField(verbose_name="Ссылка на видео")
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title


class Subscription(models.Model):
    """Модель подписки пользователя на обновления курса"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="subscriptions",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name="subscriptions",
    )
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата подписки"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = (
            "user",
            "course",
        )  # Один пользователь может подписаться на курс только один раз

    def __str__(self):
        return f'{self.user.email} подписан на "{self.course.title}"'
