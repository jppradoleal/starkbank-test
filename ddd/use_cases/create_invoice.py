import abc
from ddd.domain.invoice import Invoice


class CreateInvoice(abc.ABC):
    @abc.abstractmethod
    def create(self, invoice: Invoice):
        ...
