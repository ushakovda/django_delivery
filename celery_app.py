from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_delivery.settings')

app = Celery('django_delivery')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update_delivery_cost_every_5_minutes': {
        'task': 'registration.tasks.update_delivery_cost',
        'schedule': crontab(minute='*/5'),
    },
}

#  celery -A celery_app worker --loglevel=info