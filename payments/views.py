from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from payments import exceptions

from .services import starkbank_service


class WebhookViewSet(viewsets.ViewSet):
    def create(self, request: Request):
        digital_signature = request._request.headers.get("Digital-Signature")
        data = request._request.body.decode("utf-8")

        try:
            starkbank_service.handle_invoice_event(data, digital_signature)
        except exceptions.InvalidSignatureError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except exceptions.EventNotHandledError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
