from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from starkbank import Event, error

from .services import starkbank_service


class WebhookViewSet(viewsets.ViewSet):
    def create(self, request: Request):
        digital_signature = request._request.headers.get("Digital-Signature")

        if not digital_signature:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            event: Event = starkbank_service.parse_event(
                request._request.body.decode("utf-8"), digital_signature
            )
        except error.InvalidSignatureError:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if event["subscription"] != "invoice":
            return Response(status=status.HTTP_400_BAD_REQUEST)

        starkbank_service.handle_invoice_event(event["log"]["invoice"])
        return Response(status=status.HTTP_200_OK)
