from ..services import starkbank_service
from unittest.mock import patch
from ddd.domain import Invoice, Transfer, AccountType


def test_create_invoices(faker):
    with patch("starkbank.invoice.create") as mock:
        starkbank_service.create_invoices(
            [
                Invoice(
                    amount=100,
                    tax_id=faker.cpf(),
                    name=faker.name(),
                    descriptions=[
                        {"key": "Product Description", "value": faker.text(20)},
                    ],
                )
            ]
        )

        mock.assert_called_once()


def test_create_transfer(faker):
    with patch("starkbank.transfer.create") as mock:
        starkbank_service.create_transfer(
            [
                Transfer(
                    amount=100,
                    name="Stark Bank S.A.",
                    tax_id="20.018.183/0001-80",
                    bank_code="20018183",
                    branch_code="0001",
                    account_number="6341320293482496",
                    account_type=AccountType.PAYMENT
                )
            ]
        )

        mock.assert_called_once()
