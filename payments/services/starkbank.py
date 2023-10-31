import starkbank
import os
from ddd.domain import Invoice, Transfer


class StarkbankService:
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

    def create_transfer(self, transfers: list[Transfer]):
        transfer_objects = [
            starkbank.Transfer(**transfer.asdict()) for transfer in transfers
        ]

        return starkbank.transfer.create(transfer_objects)


with open(os.getenv("STARKBANK_PRIVATE_KEY_FILE", "./stark-priv-key.pem"), "r") as f:
    STARKBANK_PRIVATE_KEY = f.read()

starkbank_service = StarkbankService(STARKBANK_PRIVATE_KEY)
