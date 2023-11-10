from unittest.mock import patch

import pytest
from starkbank import Event
from starkbank import Invoice
from starkbank import Invoice as StarkbankInvoice
from starkbank import Transfer
from starkbank.event.__event import _resource
from starkcore.utils.api import from_api_json

from payments import exceptions

from ..services import starkbank_service


class TestStarkbank:
    valid_event: Event = from_api_json(
        _resource,
        {
            "created": None,
            "is_delivered": False,
            "workspace_id": None,
            "id": "000000",
            "subscription": "invoice",
            "log": {
                "id": "00000000",
                "created": None,
                "type": None,
                "errors": None,
                "invoice": {
                    "tax_id": "",
                    "name": "Dummy",
                    "amount": 100,
                    "fee": 10,
                },
            },
        },
    )

    def test_create_invoices(self, faker):
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

    def test_create_transfer(self, faker):
        with patch("starkbank.transfer.create") as mock:
            starkbank_service.create_transfers(
                [
                    Transfer(
                        amount=100,
                        name="Stark Bank S.A.",
                        tax_id="20.018.183/0001-80",
                        bank_code="20018183",
                        branch_code="0001",
                        account_number="6341320293482496",
                        account_type="payment",
                    )
                ]
            )

            mock.assert_called_once()

    @patch(
        "payments.services.starkbank.StarkbankService.parse_event",
        return_value=valid_event,
    )
    @patch("payments.tasks.send_transfers.delay")
    def test_handle_invoice_event(self, mock_send_transfers, mock_signature, faker):
        invoice = StarkbankInvoice(tax_id="", name="Dummy", amount=100, fee=10)

        starkbank_service.handle_invoice_event(invoice, "")

        mock_signature.assert_called_once()
        mock_send_transfers.assert_called_once_with(amount=90)

    @patch("starkbank.event.parse", return_value=valid_event)
    def test_parse_event(self, mock_event_parse):
        starkbank_service.parse_event("", "")
        mock_event_parse.assert_called_once()

    def test_parse_event_invalid_signature(self):
        with pytest.raises(exceptions.InvalidSignatureError):
            starkbank_service.parse_event("", "")
