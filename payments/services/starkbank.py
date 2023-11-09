import os

import starkbank
from starkbank import Event, Invoice, Transfer, error

from payments import exceptions, tasks


class StarkbankService:
    __project = None

    def __init__(self, private_key: str) -> None:
        self.__project = starkbank.Project(
            environment="sandbox", id="6214224581754880", private_key=private_key
        )

        starkbank.user = self.__project

    def create_invoices(self, invoices: list[Invoice]) -> list[Invoice]:
        return starkbank.invoice.create(invoices)

    def create_transfers(self, transfers: list[Transfer]) -> list[Transfer]:
        return starkbank.transfer.create(transfers)

    def parse_event(self, payload: str, signature: str) -> starkbank.Event:
        try:
            event = starkbank.event.parse(payload, signature)
        except error.InvalidSignatureError:
            raise exceptions.InvalidSignatureError()

        return event

    def handle_invoice_event(self, data: str, digital_signature: str) -> None:
        event: Event = self.parse_event(data, digital_signature)

        if event.subscription != "invoice":
            raise exceptions.EventNotHandledError()

        invoice = event.log.invoice

        amount = invoice.amount
        fees = invoice.fee

        tasks.send_transfers.delay(amount=amount - fees)


def get_private_key_content() -> str:
    return os.getenv("STARKBANK_PRIVATE_KEY")


starkbank_service = StarkbankService(get_private_key_content())
