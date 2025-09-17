from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

@shared_task
def send_course_update_notification(course_id, course_title, subscribers_emails):
    """
    Отправляет уведомления подписчикам об обновлении курса
    """
    try:
        subject = f'Обновление курса: {course_title}'
        message = f'''
        Здравствуйте!
        
        Курс "{course_title}" был обновлен. 
        Новые материалы уже доступны для изучения.
        
        Переходите по ссылке: http://localhost:8000/courses/
        
        С уважением,
        Команда Studing Place
        '''
        
        from_email = settings.DEFAULT_FROM_EMAIL
        
        # Отправляем письма всем подписчикам
        for email in subscribers_emails:
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=from_email,
                    recipient_list=[email],
                    fail_silently=False,
                )
                logger.info(f'Уведомление отправлено пользователю {email} об обновлении курса {course_title}')
            except Exception as e:
                logger.error(f'Ошибка отправки письма пользователю {email}: {str(e)}')
        
        return f'Уведомления отправлены {len(subscribers_emails)} подписчикам курса {course_title}'
        
    except Exception as e:
        logger.error(f'Ошибка в задаче отправки уведомлений: {str(e)}')
        raise

@shared_task
def send_lesson_update_notification(lesson_id, lesson_title, course_title, subscribers_emails):
    """
    Отправляет уведомления подписчикам об обновлении урока
    """
    try:
        subject = f'Новый урок в курсе: {course_title}'
        message = f'''
        Здравствуйте!
        
        В курсе "{course_title}" добавлен новый урок: "{lesson_title}".
        
        Переходите по ссылке: http://localhost:8000/lessons/
        
        С уважением,
        Команда Studing Place
        '''
        
        from_email = settings.DEFAULT_FROM_EMAIL
        
        # Отправляем письма всем подписчикам
        for email in subscribers_emails:
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=from_email,
                    recipient_list=[email],
                    fail_silently=False,
                )
                logger.info(f'Уведомление отправлено пользователю {email} об обновлении урока {lesson_title}')
            except Exception as e:
                logger.error(f'Ошибка отправки письма пользователю {email}: {str(e)}')
        
        return f'Уведомления отправлены {len(subscribers_emails)} подписчикам курса {course_title}'
        
    except Exception as e:
        logger.error(f'Ошибка в задаче отправки уведомлений об уроке: {str(e)}')
        raise

@shared_task
def block_inactive_users():
    """
    Блокирует пользователей, которые не заходили более месяца
    """
    try:
        inactive_days = getattr(settings, 'INACTIVE_USER_DAYS', 30)
        cutoff_date = timezone.now() - timedelta(days=inactive_days)
        
        # Находим пользователей, которые не заходили более указанного количества дней
        inactive_users = User.objects.filter(
            last_login__lt=cutoff_date,
            is_active=True
        ).exclude(
            is_superuser=True  # Не блокируем суперпользователей
        )
        
        blocked_count = 0
        for user in inactive_users:
            user.is_active = False
            user.save()
            blocked_count += 1
            logger.info(f'Пользователь {user.email} заблокирован за неактивность')
        
        # Отправляем уведомление администраторам о заблокированных пользователях
        if blocked_count > 0:
            admin_emails = User.objects.filter(is_superuser=True).values_list('email', flat=True)
            if admin_emails:
                send_mail(
                    subject='Отчет о блокировке неактивных пользователей',
                    message=f'Заблокировано {blocked_count} неактивных пользователей.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=list(admin_emails),
                    fail_silently=False,
                )
        
        return f'Заблокировано {blocked_count} неактивных пользователей'
        
    except Exception as e:
        logger.error(f'Ошибка в задаче блокировки пользователей: {str(e)}')
        raise

@shared_task
def send_welcome_email(user_email, user_name):
    """
    Отправляет приветственное письмо новому пользователю
    """
    try:
        subject = 'Добро пожаловать в Studing Place!'
        message = f'''
        Здравствуйте, {user_name}!
        
        Добро пожаловать в Studing Place - платформу для онлайн-обучения!
        
        Теперь вы можете:
        - Просматривать доступные курсы
        - Подписываться на обновления интересующих курсов
        - Отслеживать свой прогресс обучения
        
        Начните обучение: http://localhost:8000/courses/
        
        С уважением,
        Команда Studing Place
        '''
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        
        logger.info(f'Приветственное письмо отправлено пользователю {user_email}')
        return f'Приветственное письмо отправлено пользователю {user_email}'
        
    except Exception as e:
        logger.error(f'Ошибка отправки приветственного письма: {str(e)}')
        raise
