from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Course, Lesson
from users.models import Subscription
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_course_update_notification_async(course_id):
    """
    Асинхронная отправка уведомлений об обновлении курса
    """
    try:
        course = Course.objects.get(id=course_id)
        
        # Получаем всех подписчиков курса
        subscribers = Subscription.objects.filter(course=course, is_active=True)
        subscribers_emails = [sub.user.email for sub in subscribers if sub.user.email]
        
        if not subscribers_emails:
            logger.info(f'У курса {course.title} нет подписчиков для уведомлений')
            return f'У курса {course.title} нет подписчиков'
        
        # Отправляем уведомления
        subject = f'Обновление курса: {course.title}'
        message = f'''
        Здравствуйте!
        
        Курс "{course.title}" был обновлен. 
        Новые материалы уже доступны для изучения.
        
        Описание: {course.description[:200]}...
        
        Переходите по ссылке: http://localhost:8000/courses/{course.id}/
        
        С уважением,
        Команда Studing Place
        '''
        
        from_email = settings.DEFAULT_FROM_EMAIL
        
        # Отправляем письма всем подписчикам
        sent_count = 0
        for email in subscribers_emails:
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=from_email,
                    recipient_list=[email],
                    fail_silently=False,
                )
                sent_count += 1
                logger.info(f'Уведомление отправлено пользователю {email} об обновлении курса {course.title}')
            except Exception as e:
                logger.error(f'Ошибка отправки письма пользователю {email}: {str(e)}')
        
        return f'Уведомления отправлены {sent_count} из {len(subscribers_emails)} подписчиков курса {course.title}'
        
    except Course.DoesNotExist:
        logger.error(f'Курс с ID {course_id} не найден')
        return f'Курс с ID {course_id} не найден'
    except Exception as e:
        logger.error(f'Ошибка в задаче отправки уведомлений о курсе: {str(e)}')
        raise

@shared_task
def send_lesson_update_notification_async(lesson_id):
    """
    Асинхронная отправка уведомлений об обновлении урока
    """
    try:
        lesson = Lesson.objects.get(id=lesson_id)
        course = lesson.course
        
        # Проверяем, что курс не обновлялся более 4 часов
        four_hours_ago = timezone.now() - timedelta(hours=4)
        if course.updated_at > four_hours_ago:
            logger.info(f'Курс {course.title} обновлялся менее 4 часов назад, уведомления не отправляются')
            return f'Курс {course.title} обновлялся менее 4 часов назад'
        
        # Получаем всех подписчиков курса
        subscribers = Subscription.objects.filter(course=course, is_active=True)
        subscribers_emails = [sub.user.email for sub in subscribers if sub.user.email]
        
        if not subscribers_emails:
            logger.info(f'У курса {course.title} нет подписчиков для уведомлений')
            return f'У курса {course.title} нет подписчиков'
        
        # Отправляем уведомления
        subject = f'Новый урок в курсе: {course.title}'
        message = f'''
        Здравствуйте!
        
        В курсе "{course.title}" добавлен новый урок: "{lesson.title}".
        
        Описание урока: {lesson.description[:200] if lesson.description else 'Описание отсутствует'}...
        
        Переходите по ссылке: http://localhost:8000/lessons/{lesson.id}/
        
        С уважением,
        Команда Studing Place
        '''
        
        from_email = settings.DEFAULT_FROM_EMAIL
        
        # Отправляем письма всем подписчикам
        sent_count = 0
        for email in subscribers_emails:
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=from_email,
                    recipient_list=[email],
                    fail_silently=False,
                )
                sent_count += 1
                logger.info(f'Уведомление отправлено пользователю {email} об обновлении урока {lesson.title}')
            except Exception as e:
                logger.error(f'Ошибка отправки письма пользователю {email}: {str(e)}')
        
        return f'Уведомления отправлены {sent_count} из {len(subscribers_emails)} подписчиков курса {course.title}'
        
    except Lesson.DoesNotExist:
        logger.error(f'Урок с ID {lesson_id} не найден')
        return f'Урок с ID {lesson_id} не найден'
    except Exception as e:
        logger.error(f'Ошибка в задаче отправки уведомлений об уроке: {str(e)}')
        raise

@shared_task
def cleanup_old_courses():
    """
    Очистка старых неактивных курсов (дополнительная задача)
    """
    try:
        # Находим курсы, которые не обновлялись более года и не имеют подписчиков
        one_year_ago = timezone.now() - timedelta(days=365)
        
        old_courses = Course.objects.filter(
            updated_at__lt=one_year_ago,
            subscriptions__isnull=True  # Нет подписчиков
        )
        
        deleted_count = 0
        for course in old_courses:
            course_title = course.title
            course.delete()
            deleted_count += 1
            logger.info(f'Удален старый курс: {course_title}')
        
        return f'Удалено {deleted_count} старых курсов'
        
    except Exception as e:
        logger.error(f'Ошибка в задаче очистки старых курсов: {str(e)}')
        raise
