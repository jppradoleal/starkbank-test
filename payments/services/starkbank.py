import os

import starkbank
from starkbank import Invoice, Transfer

from payments import tasks


class StarkbankService:
    __project = None

    def __init__(self, private_key) -> None:
        self.__project = starkbank.Project(
            environment="sandbox", id="6214224581754880", private_key=private_key
        )

        starkbank.user = self.__project

    def create_invoices(self, invoices: list[Invoice]):
        return starkbank.invoice.create(invoices)

    def create_transfers(self, transfers: list[Transfer]):
        return starkbank.transfer.create(transfers)

    def parse_event(self, payload, signature) -> starkbank.Event:
        return starkbank.event.parse(payload, signature)

    def handle_invoice_event(self, invoice):
        amount = invoice.amount
        fees = invoice.fee

        tasks.send_transfers.delay(amount=amount - fees)


def get_private_key_content():
    return os.getenv("STARKBANK_PRIVATE_KEY")


starkbank_service = StarkbankService(get_private_key_content())
