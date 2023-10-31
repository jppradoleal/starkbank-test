import abc

from ddd.domain import Invoice


class CreateInvoice(abc.ABC):
    @abc.abstractmethod
    def create_invoices(self, invoices: list[Invoice]):
        ...
