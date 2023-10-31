import abc
from ddd.domain import Transfer


class CreateTransfer(abc.ABC):
    @abc.abstractmethod
    def create_transfers(self, transfers: list[Transfer]):
        ...
