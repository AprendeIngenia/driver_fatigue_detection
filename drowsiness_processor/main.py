import numpy as np
from drowsiness_processor.extract_points.main_point_extractor import PointExtractor


class DrowsinessDetectionSystem:
    def __init__(self):
        self.point_extractor = PointExtractor()

    def frame_processing(self, face_image: np.ndarray):
        face_points, control_process, original_image = self.point_extractor.process(face_image)
        return original_image
