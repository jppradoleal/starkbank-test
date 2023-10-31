import starkbank
import os
from ddd.domain import Invoice, Transfer
from ddd.use_cases import CreateInvoice, CreateTransfer, ParseEvent, HandleInvoiceEvent
from payments import tasks


class StarkbankService(CreateInvoice, CreateTransfer, ParseEvent, HandleInvoiceEvent):
    __project = None

    def __init__(self, private_key) -> None:
        self.__project = starkbank.Project(
            environment="sandbox", id="6214224581754880", private_key=private_key
        )

        starkbank.user = self.__project

    def create_invoices(self, invoices: list[Invoice]):
        invoice_objects = [
            starkbank.Invoice(**invoice.asdict()) for invoice in invoices
        ]

        return starkbank.invoice.create(invoice_objects)

    def create_transfers(self, transfers: list[Transfer]):
        transfer_objects = [
            starkbank.Transfer(**transfer.asdict()) for transfer in transfers
        ]

        return starkbank.transfer.create(transfer_objects)

    def parse_event(self, payload, signature) -> starkbank.Event:
        return starkbank.event.parse(payload, signature)

    def handle_invoice_event(self, invoice):
        amount = invoice["amount"]
        fees = invoice["fee"]

        tasks.send_transfers.delay(amount=amount - fees)


def get_private_key_content():
    with open(
        os.getenv("STARKBANK_PRIVATE_KEY_FILE", "./stark-priv-key.pem"), "r"
    ) as f:
        private_key_content = f.read()
    return private_key_content


starkbank_service = StarkbankService(get_private_key_content())
