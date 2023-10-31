import os

from celery import Celery

from payments import tasks

_ONE_HOUR_IN_SECONDS = 60 * 60
_SEND_INVOICES_FREQUENCY = (_ONE_HOUR_IN_SECONDS / 60) / 2 # Runs one time every 30 seconds - FOR TESTING PURPOUSES
#_SEND_INVOICES_FREQUENCY = 3 * _ONE_HOUR_IN_SECONDS # Runs one time every 3 hours

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'starkbank_backend.settings')
app = Celery('starkbank_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
  sender.add_periodic_task(
    _SEND_INVOICES_FREQUENCY,
    tasks.send_invoices.s(),
    name='send invoices every 3 hours',
  )
