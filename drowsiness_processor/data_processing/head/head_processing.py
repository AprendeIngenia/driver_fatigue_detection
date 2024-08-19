import numpy as np
from abc import ABC, abstractmethod


class DistanceCalculator(ABC):
    @abstractmethod
    def calculate_distance(self, point1, point2):
        pass


class EuclideanDistanceCalculator(DistanceCalculator):
    def calculate_distance(self, point1, point2):
        point1 = point1[1]
        point2 = point2[1]
        return np.linalg.norm(point1 - point2)


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
        nose_mouth_distance, nose_head_distance = self.calculate_distances(head_points)
        self.head['nose_mouth_distance'] = nose_mouth_distance
        self.head['nose_head_distance'] = nose_head_distance
        self.head['nose_point'] = head_points['distances'][4]
        self.head['right_cheek_point'] = head_points['distances'][5]
        self.head['left_cheek_point'] = head_points['distances'][6]
        return self.head
