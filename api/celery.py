import os

from django.conf import settings

from celery import Celery


if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

app = Celery('starter')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
