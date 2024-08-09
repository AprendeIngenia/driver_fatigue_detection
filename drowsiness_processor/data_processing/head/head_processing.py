import numpy as np
from abc import ABC, abstractmethod


class DistanceCalculator(ABC):
    @abstractmethod
    def calculate_distance(self, point1, point2):
        pass


class EuclideanDistanceCalculator(DistanceCalculator):
    def calculate_distance(self, point1, point2):
        return np.linalg.norm(np.array(point1) - np.array(point2))


class HeadPointsProcessing:
    def __init__(self, distance_calculator: DistanceCalculator):
        self.distance_calculator = distance_calculator
        self.head: dict = {}

    def calculate_distances(self, head_points: dict):
        nose_mouth = self.distance_calculator.calculate_distance(head_points['distances'][0],
                                                                 head_points['distances'][1])
        head_front = self.distance_calculator.calculate_distance(head_points['distances'][2],
                                                                 head_points['distances'][3])
        return nose_mouth, head_front

    def main(self, head_points: dict):
        nose_mouth_distance, head_front_distance = self.calculate_distances(head_points)
        self.head['nose_mouth_distance'] = nose_mouth_distance
        self.head['head_front_distance'] = head_front_distance
        return self.head
