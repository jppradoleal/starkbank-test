from celery import shared_task
from random import randint
from ddd.domain import Invoice, Transfer, AccountType
from faker import Faker
from .services import starkbank_service
from celery_batches import Batches
import starkbank


@shared_task(
    soft_time_limit=15,
    time_limit=30,
    autoretry_for=(starkbank.error.InternalServerError, starkbank.error.UnknownError,),
    retry_backoff=True,
    retry_kwargs={'max_retries': 3})
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
    autoretry_for=(starkbank.error.InternalServerError, starkbank.error.UnknownError,),
    retry_backoff=True,
    retry_kwargs={'max_retries': 3})
def send_transfers(requests):
    amounts = [request.kwargs["amount"] for request in requests]
    
    print(f"Transfering: {amounts}")
    
    transfer = Transfer(
        amount=sum(amounts),
        account_number="6341320293482496",
        account_type=AccountType.PAYMENT,
        bank_code="20018183",
        branch_code="0001",
        tax_id="20.018.183/0001-80",
        name="Stark Bank S.A."
    )

    starkbank_service.create_transfers([transfer])
