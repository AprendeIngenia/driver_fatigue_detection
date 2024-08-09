import numpy as np
from drowsiness_processor.extract_points.point_extractor import PointsExtractor
from drowsiness_processor.data_processing.main import PointsProcessing


class DrowsinessDetectionSystem:
    def __init__(self):
        self.points_extractor = PointsExtractor()
        self.points_processing = PointsProcessing()

    def frame_processing(self, face_image: np.ndarray):
        key_points, control_process, sketch = self.points_extractor.process(face_image)
        if control_process:
            points_processed = self.points_processing.main(key_points)
            print(points_processed)
        return face_image, sketch
