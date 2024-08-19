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


class EyesPointsProcessing:
    def __init__(self, distance_calculator: DistanceCalculator):
        self.distance_calculator = distance_calculator
        self.eyes: dict = {}

    def calculate_distances(self, eyes_points: dict):
        right_upper_eyelid = self.distance_calculator.calculate_distance(eyes_points['distances'][0],
                                                                         eyes_points['distances'][1])
        left_upper_eyelid = self.distance_calculator.calculate_distance(eyes_points['distances'][2],
                                                                        eyes_points['distances'][3])
        right_lower_eyelid = self.distance_calculator.calculate_distance(eyes_points['distances'][4],
                                                                         eyes_points['distances'][5])
        left_lower_eyelid = self.distance_calculator.calculate_distance(eyes_points['distances'][6],
                                                                        eyes_points['distances'][7])
        return right_upper_eyelid, left_upper_eyelid, right_lower_eyelid, left_lower_eyelid

    def main(self, eyes_points: dict):
        (right_upper_eyelid_distance, left_upper_eyelid_distance, right_lower_eyelid_distance,
         left_lower_eyelid_distance) = self.calculate_distances(eyes_points)
        self.eyes['right_upper_eyelid_distance'] = right_upper_eyelid_distance
        self.eyes['left_upper_eyelid_distance'] = left_upper_eyelid_distance
        self.eyes['right_lower_eyelid_distance'] = right_lower_eyelid_distance
        self.eyes['left_lower_eyelid_distance'] = left_lower_eyelid_distance
        return self.eyes
