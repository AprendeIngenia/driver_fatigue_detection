import numpy as np
from drowsiness_processor.extract_points.point_extractor import PointsExtractor
from drowsiness_processor.data_processing.main import PointsProcessing
from drowsiness_processor.drowsiness.processing import FeaturesDrowsinessProcessing


class DrowsinessDetectionSystem:
    def __init__(self):
        self.points_extractor = PointsExtractor()
        self.points_processing = PointsProcessing()
        self.features_processing = FeaturesDrowsinessProcessing()

    def frame_processing(self, face_image: np.ndarray):
        key_points, control_process, sketch = self.points_extractor.process(face_image)
        if control_process:
            points_processed = self.points_processing.main(key_points)
            #print(points_processed)
            drowsiness_info = self.features_processing.main(points_processed)
            #print(drowsiness_info)

        return face_image, sketch
