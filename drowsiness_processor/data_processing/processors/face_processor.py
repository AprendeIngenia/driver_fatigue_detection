from abc import ABC, abstractmethod


class FaceProcessor(ABC):
    @abstractmethod
    def process(self, points: dict):
        raise NotImplemented
