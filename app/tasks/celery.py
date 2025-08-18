from datetime import timedelta
from celery import Celery
from celery.schedules import crontab
from app.config import settings


celery_app = Celery(
    'myvkfeed_tasks',
    broker=settings.celery.broker_url,
    include=['app.tasks.beat_tasks'],
    broker_connection_retry_on_startup=True
)


celery_app.conf.beat_schedule = {
    'clear_expired_refresh_tokens': {
        'task': 'clear_expired_refresh_tokens',
        'schedule': timedelta(minutes=1) # crontab(hour='0', minute='0'),
    },
}