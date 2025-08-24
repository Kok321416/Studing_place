from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название курса')
    preview = models.ImageField(upload_to='course/', verbose_name='Превью курса')
    description = models.TextField(verbose_name='Описание курса')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title

class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название урока')
    preview = models.ImageField(upload_to='lesson_previews/', verbose_name='Превью')
    description = models.TextField(verbose_name='Описание урока')
    video_link = models.URLField(verbose_name='Ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title

