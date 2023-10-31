import abc


class HandleInvoiceEvent(abc.ABC):
    @abc.abstractmethod
    def handle_invoice_event(self, invoice):
        ...
