import os

from celery import Celery
from django.conf import settings

from payments import tasks

_ONE_HOUR_IN_SECONDS = 60 * 60
_SEND_INVOICES_FREQUENCY = (_ONE_HOUR_IN_SECONDS / 60) / 2 # Runs one time every 30 seconds - FOR TESTING PURPOUSES
#_SEND_INVOICES_FREQUENCY = 3 * _ONE_HOUR_IN_SECONDS # Runs one time every 3 hours

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'starkbank_backend.settings')
app = Celery('starkbank_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
