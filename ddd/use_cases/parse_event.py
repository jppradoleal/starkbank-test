import abc


class ParseEvent(abc.ABC):
    @abc.abstractmethod
    def parse_event(self, payload, signature):
        ...
