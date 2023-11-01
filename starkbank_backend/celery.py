import os

from celery import Celery

from payments import tasks

INVOICE_TASK_FREQUENCY = int(os.getenv("INVOICE_TASK_FREQUENCY", 60 * 60 * 3))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "starkbank_backend.settings")
app = Celery("starkbank_backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        INVOICE_TASK_FREQUENCY,
        tasks.send_invoices.s(),
        name="send invoices every 3 hours",
    )
