import numpy as np
from abc import ABC, abstractmethod


class DistanceCalculator(ABC):
    @abstractmethod
    def calculate_distance(self, point1, point2):
        pass


class EuclideanDistanceCalculator(DistanceCalculator):
    def calculate_distance(self, point1, point2):
        return np.linalg.norm(np.array(point1) - np.array(point2))


class FingerEyeDistanceCalculator:
    def __init__(self, distance_calculator: DistanceCalculator):
        self.distance_calculator = distance_calculator

    def calculate_finger_eye_distances(self, finger_points: dict, eye_point: list) -> dict:
        return {
            'thumb': self.distance_calculator.calculate_distance(finger_points[0], eye_point),
            'index_finger': self.distance_calculator.calculate_distance(finger_points[1], eye_point),
            'middle_finger': self.distance_calculator.calculate_distance(finger_points[2], eye_point),
            'ring_finger': self.distance_calculator.calculate_distance(finger_points[3], eye_point),
            'little_finger': self.distance_calculator.calculate_distance(finger_points[4], eye_point),
        }


class FirstHandPointsProcessing:
    def __init__(self, distance_calculator: DistanceCalculator):
        self.distance_calculator = distance_calculator
        self.finger_eye_calculator = FingerEyeDistanceCalculator(distance_calculator)
        self.hands: dict = {}

    def main(self, hand_points: dict, eyes_points: dict):
        self.hands['hand_to_right_eye'] = self.finger_eye_calculator.calculate_finger_eye_distances(hand_points[
                                                                                                        'distances'],
                                                                                                    eyes_points[
                                                                                                        'distances'][8])
        self.hands['hand_to_left_eye'] = self.finger_eye_calculator.calculate_finger_eye_distances(hand_points[
                                                                                                       'distances'],
                                                                                                   eyes_points[
                                                                                                       'distances'][9])
        return self.hands
