import numpy as np
from typing import Tuple
import logging as log
from drowsiness_processor.extract_points.face_mesh.face_mesh_processor import FaceMeshProcessor
from drowsiness_processor.extract_points.hands.hands_processor import HandsProcessor


log.basicConfig(level=log.INFO)
logger = log.getLogger(__name__)


class PointsExtractor:
    def __init__(self):
        self.face_mesh = FaceMeshProcessor()
        self.hands = HandsProcessor()

    def process(self, face_image: np.ndarray) -> Tuple[dict, bool, np.ndarray]:
        face_points, mesh_success, draw_sketch = self.face_mesh.process(face_image, draw=True)
        if mesh_success:
            hands_points, hands_success, draw_sketch = self.hands.process(face_image, draw_sketch, draw=True)
            if hands_success:
                merged_points = self.merge_points(face_points, hands_points)
                #logger.info(
                #    "Face mesh: successful.\nHands detect: succesfull. \nExtract: blinks, microsleeps, yawning, "
                #    "nodding, eye rubbing")
                return merged_points, True, draw_sketch
            else:
                #logger.info(
                #    "Face mesh: successful.\nHands detect: failed. \nExtract: blinks, microsleeps, yawning, nodding")
                return face_points, True, draw_sketch
        else:
            #logger.warning("Face mesh: failed, no drowsiness_features recognition.")
            return face_points, False, draw_sketch

    def merge_points(self, face_points: dict, hands_points: dict) -> dict:
        merged_points = {**face_points, **hands_points}
        return merged_points
