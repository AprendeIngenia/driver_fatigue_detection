from drowsiness_processor.data_processing.processors.face_processor import FaceProcessor
from drowsiness_processor.data_processing.eyes.eyes_processing import (EyesPointsProcessing,
                                                                       EuclideanDistanceCalculator)


class EyesProcessor(FaceProcessor):
    def __init__(self):
        distance_calculator = EuclideanDistanceCalculator()
        self.processor = EyesPointsProcessing(distance_calculator)

    def process(self, points: dict):
        return self.processor.main(points)
