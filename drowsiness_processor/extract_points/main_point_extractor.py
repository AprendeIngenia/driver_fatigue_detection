import numpy as np
from typing import Tuple
from drowsiness_processor.extract_points.face_mesh.face_mesh_processor import FaceMeshProcessor
from drowsiness_processor.extract_points.hands.hands_processor import HandsProcessor


class PointExtractor:
    def __init__(self):
        self.face_mesh = FaceMeshProcessor()
        self.hands = HandsProcessor()

    def process(self, face_image: np.ndarray) -> Tuple[dict, bool, np.ndarray]:
        face_points, mesh_success, draw_mesh_image = self.face_mesh.process(face_image, draw=True)
        if mesh_success:
            hands_points, hands_success, draw_hands_image = self.hands.process(face_image, draw=True)
            if hands_success:
                print('MERGE FACE AND HANDS')
                print(hands_points, face_points)
            return face_points, mesh_success, draw_mesh_image
        return face_points, mesh_success, draw_mesh_image
