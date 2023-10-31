import abc
from domain.transfer import Transfer


class CreateTransfer(abc.ABC):
    @abc.abstractmethod
    def create(self, transfer: Transfer):
        ...
