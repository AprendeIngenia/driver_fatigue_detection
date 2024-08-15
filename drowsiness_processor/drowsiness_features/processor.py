from abc import ABC, abstractmethod


class DrowsinessProcessor(ABC):
    @abstractmethod
    def process(self, points: dict):
        raise NotImplemented
