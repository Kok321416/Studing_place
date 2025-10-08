import os
from celery import Celery

# Устанавливаем переменную окружения для Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

# Загружаем конфигурацию из settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически находим и регистрируем задачи
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
