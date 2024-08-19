import mediapipe as mp
import numpy as np
import cv2
from typing import Tuple, Any, List, Dict


class FaceMeshInference:
    def __init__(self, min_detection_confidence=0.6, min_tracking_confidence=0.6):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

    def process(self, image: np.ndarray) -> Tuple[bool, Any]:
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_mesh = self.face_mesh.process(rgb_image)
        return bool(face_mesh.multi_face_landmarks), face_mesh


class FaceMeshExtractor:
    def __init__(self):
        self.points: dict = {
            'eyes': {'distances': []},
            'mouth': {'distances': []},
            'head': {'distances': []},
        }

    def extract_points(self, face_image: np.ndarray, face_mesh_info: Any) -> List[List[int]]:
        h, w, _ = face_image.shape
        mesh_points = [
            [i, int(pt.x * w), int(pt.y * h)]
            for face in face_mesh_info.multi_face_landmarks
            for i, pt in enumerate(face.landmark)
        ]
        return mesh_points

    def extract_feature_points(self, face_points: List[List[int]], feature_indices: dict):
        for feature, indices in feature_indices.items():
            for sub_feature, sub_indices in indices.items():
                self.points[feature][sub_feature] = [face_points[i][1:] for i in sub_indices]

    def get_eyes_points(self, face_points: List[List[int]]) -> Dict[str, List[List[int]]]:
        feature_indices = {
            'eyes': {
                'distances': [159, 145, 385, 374, 468, 472, 473, 477, 468, 473],
            }
        }
        self.extract_feature_points(face_points, feature_indices)
        return self.points['eyes']

    def get_mouth_points(self, face_points: List[List[int]]) -> Dict[str, List[List[int]]]:
        feature_indices = {
            'mouth': {
                'distances': [13, 14, 17, 199]
            }
        }
        self.extract_feature_points(face_points, feature_indices)
        return self.points['mouth']

    def get_head_points(self, face_points: List[List[int]]) -> Dict[str, List[List[int]]]:
        feature_indices = {
            'head': {
                'distances': [1, 0, 1, 5, 4, 205, 425]
            }
        }
        self.extract_feature_points(face_points, feature_indices)
        return self.points['head']


class FaceMeshDrawer:
    def __init__(self, color: Tuple[int, int, int] = (255, 255, 0)):
        self.mp_draw = mp.solutions.drawing_utils
        self.config_draw = self.mp_draw.DrawingSpec(color=color, thickness=1, circle_radius=1)

    def draw(self, face_image: np.ndarray, face_mesh_info: Any):
        for face_mesh in face_mesh_info.multi_face_landmarks:
            self.mp_draw.draw_landmarks(face_image, face_mesh, mp.solutions.face_mesh.FACEMESH_TESSELATION,
                                        self.config_draw, self.config_draw)

    def draw_sketch(self, face_image: np.ndarray, face_mesh_info: Any):
        h, w, _ = face_image.shape
        black_image = np.zeros((h, w, 3), dtype=np.uint8)
        for face_mesh in face_mesh_info.multi_face_landmarks:
            for pt in face_mesh.landmark:
                x = int(pt.x * w)
                y = int(pt.y * h)
                z = int(pt.z * 50)
                cv2.circle(black_image, (x, y), 1, (255 - z, 255 - z, 0 - z), -1)
        return black_image


class FaceMeshProcessor:
    def __init__(self):
        self.inference = FaceMeshInference()
        self.extractor = FaceMeshExtractor()
        self.drawer = FaceMeshDrawer()

    def process(self, face_image: np.ndarray, draw: bool = True) -> Tuple[dict, bool, np.ndarray]:
        h, w, _ = face_image.shape
        sketch = np.zeros((h, w, 3), dtype=np.uint8)
        success, face_mesh_info = self.inference.process(face_image)
        if not success:
            return {}, success, sketch

        face_points = self.extractor.extract_points(face_image, face_mesh_info)
        points = {
            'eyes': self.extractor.get_eyes_points(face_points),
            'mouth': self.extractor.get_mouth_points(face_points),
            'head': self.extractor.get_head_points(face_points),
        }

        if draw:
            sketch = self.drawer.draw_sketch(face_image, face_mesh_info)
            return points, success, sketch

        return points, success, sketch
