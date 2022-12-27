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

# app.conf.beat_schedule = {
#     'run-every-single-minute': {
#         'task': 'testapp.tasks.hello_world',
#         'schedule': crontab(),
#     },
# }
