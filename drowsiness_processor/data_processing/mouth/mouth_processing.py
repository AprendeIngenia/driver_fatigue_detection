import numpy as np
from abc import ABC, abstractmethod


class DistanceCalculator(ABC):
    @abstractmethod
    def calculate_distance(self, point1, point2):
        pass


class EuclideanDistanceCalculator(DistanceCalculator):
    def calculate_distance(self, point1, point2):
        return np.linalg.norm(np.array(point1) - np.array(point2))


class MouthPointsProcessing:
    def __init__(self, distance_calculator: DistanceCalculator):
        self.distance_calculator = distance_calculator
        self.mouth: dict = {}

    def calculate_distances(self, mouth_points: dict):
        lips = self.distance_calculator.calculate_distance(mouth_points['distances'][0],
                                                           mouth_points['distances'][1])
        chin = self.distance_calculator.calculate_distance(mouth_points['distances'][2],
                                                           mouth_points['distances'][3])
        return lips, chin

    def main(self, mouth_points: dict):
        lips_distance, chin_distance = self.calculate_distances(mouth_points)
        self.mouth['lips_distance'] = lips_distance
        self.mouth['chin_distance'] = chin_distance
        return self.mouth
