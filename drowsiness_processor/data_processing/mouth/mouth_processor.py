from drowsiness_processor.data_processing.processors.face_processor import FaceProcessor
from drowsiness_processor.data_processing.mouth.mouth_processing import (EuclideanDistanceCalculator,
                                                                         MouthPointsProcessing)


class MouthProcessor(FaceProcessor):
    def __init__(self):
        distance_calculator = EuclideanDistanceCalculator()
        self.processor = MouthPointsProcessing(distance_calculator)

    def process(self, points: dict):
        return self.processor.main(points)
