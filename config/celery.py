import os
from celery import Celery
from django.conf import settings

# Устанавливаем переменную окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создаем экземпляр Celery
app = Celery('studing_place')

# Используем строку для автоматического обнаружения задач
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач из всех приложений Django
app.autodiscover_tasks()

# Настройки для celery-beat
app.conf.beat_schedule = {
    'block-inactive-users': {
        'task': 'users.tasks.block_inactive_users',
        'schedule': 60.0 * 60.0 * 24.0,  # Каждый день (24 часа)
        'options': {
            'timezone': 'Europe/Moscow',
        }
    },
}

# Настройки timezone
app.conf.timezone = 'Europe/Moscow'

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
