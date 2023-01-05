import os
import django

from celery import Celery
from django.conf import settings

from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

app = Celery('config')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'send_spam': {
        'task': 'applications.account.tasks.send_spam',
        'schedule': crontab(day_of_week='*/7'),
    },
    'delete_music': {
        'task': 'applications.product.tasks.delete_not_paid_music',
        'schedule': crontab(day_of_week='*/7'),
    },
}
