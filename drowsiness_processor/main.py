import numpy as np
from drowsiness_processor.extract_points.point_extractor import PointExtractor


class DrowsinessDetectionSystem:
    def __init__(self):
        self.point_extractor = PointExtractor()

    def frame_processing(self, face_image: np.ndarray):
        key_points, control_process, sketch_image = self.point_extractor.process(face_image)
        return face_image, sketch_image
