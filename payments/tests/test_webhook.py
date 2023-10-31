from unittest.mock import patch, MagicMock
from django.test.client import Client
from starkbank.error import InvalidSignatureError
from rest_framework.reverse import reverse


class TestWebhook:
    endpoint = reverse("webhook-list")

    @patch("payments.tasks.send_transfers.delay")
    @patch(
        "starkbank.event.parse",
        return_value={
            "subscription": "invoice",
            "log": {"invoice": {"amount": 100, "fee": 10}},
        },
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
        return_value={
            "subscription": "boleto",
            "log": {"boleto": {"amount": 100, "fee": 10}},
        },
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

    @patch(
        "starkbank.event.parse",
    )
    @patch("payments.tasks.send_transfers.delay")
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
