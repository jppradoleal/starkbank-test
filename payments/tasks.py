from celery import shared_task
from random import randint
from ddd.domain.invoice import Invoice
from faker import Faker
from .services import starkbank_service
from celery_batches import Batches


@shared_task(soft_time_limit=15, time_limit=30, retry_backoff=True, retry_kwargs={'max_retries': 3})
def send_invoices():
    fake = Faker("pt-BR")
    invoices = [
        Invoice(
            name=fake.name(),
            amount=randint(1000, 10000),
            descriptions=[{"key": "Product Description", "value": fake.text(20)}],
            tax_id=fake.cpf(),
        )
        for _ in range(randint(8, 12))
    ]

    print(f"Sending {len(invoices)} invoices")

    starkbank_service.create_invoices(invoices)


@shared_task(
    base=Batches,
    flush_every=15,
    flush_interval=10,
    soft_time_limit=15,
    time_limit=30,
    retry_backoff=True,
    retry_kwargs={'max_retries': 3})
def send_transfers(transfer):
    starkbank_service.create_transfer([transfer])
