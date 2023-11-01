from unittest.mock import MagicMock, patch

from django.test.client import Client
from rest_framework.reverse import reverse
from starkbank.error import InvalidSignatureError
from starkbank.event.__event import _resource
from starkcore.utils.api import from_api_json


class TestWebhook:
    endpoint = reverse("webhook-list")

    @patch("payments.tasks.send_transfers.delay")
    @patch(
        "starkbank.event.parse",
        return_value=from_api_json(
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
        ),
    )
    def test_webhook_runs(
        self,
        mock_event_parse: MagicMock,
        mock_send_transfers_task: MagicMock,
        client: Client,
    ):
        data = {}
        headers = {"HTTP_DIGITAL_SIGNATURE": "abc"}
        response = client.post(self.endpoint, data=data, **headers)

        mock_event_parse.assert_called_once()

        mock_send_transfers_task.assert_called_once_with(amount=100 - 10)

        assert response.status_code == 200

    @patch("payments.tasks.send_transfers.delay")
    @patch(
        "starkbank.event.parse",
        return_value=from_api_json(
            _resource,
            {
                "created": None,
                "is_delivered": False,
                "workspace_id": None,
                "id": "000000",
                "subscription": "boleto",
                "log": {
                    "id": "00000000",
                    "created": None,
                    "type": None,
                    "errors": None,
                    "boleto": {"tax_id": "", "name": "Dummy", "amount": 100, "fee": 10},
                },
            },
        ),
    )
    def test_webhook_process_invoice_events_only(
        self,
        mock_event_parse: MagicMock,
        mock_2: MagicMock,
        client: Client,
    ):
        data = {}
        headers = {"HTTP_DIGITAL_SIGNATURE": "abc"}
        response = client.post(self.endpoint, data=data, **headers)

        mock_event_parse.assert_called_once()

        assert response.status_code == 400

    @patch("payments.tasks.send_transfers.delay")
    @patch("starkbank.event.parse")
    def test_webhook_ignores_request_without_signature(self, mock_1, mock_2, client):
        data = {}
        response = client.post(self.endpoint, data=data)

        assert response.status_code == 404

    @patch("payments.tasks.send_transfers.delay")
    @patch(
        "starkbank.event.parse",
        side_effect=InvalidSignatureError(""),
    )
    def test_webhook_ignores_request_with_invalid_signature(
        self, mock_event_parse: MagicMock, mock_2, client
    ):
        data = {}
        headers = {"HTTP_DIGITAL_SIGNATURE": "invalid"}
        response = client.post(self.endpoint, data=data, **headers)

        mock_event_parse.assert_called_once()
        assert response.status_code == 404
