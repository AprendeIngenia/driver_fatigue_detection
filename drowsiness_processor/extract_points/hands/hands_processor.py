import numpy as np
import mediapipe as mp
import cv2
from typing import Tuple, Any, List, Dict


class HandsInference:
    def __init__(self, min_detection_confidence=0.6, min_tracking_confidence=0.6):
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            model_complexity=1,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

    def process(self, image: np.ndarray) -> Tuple[bool, Any]:
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        hands = self.hands.process(rgb_image)
        return bool(hands.multi_hand_landmarks), hands


class HandsExtractor:
    def __init__(self):
        self.points: dict = {
            'fingers': {'distances': []},
        }

    def count_hands(self, hands_info):
        return len(hands_info.multi_hand_landmarks)

    def extract_points(self, face_image: np.ndarray, hands_info: Any, hand_index: int = 0) -> List[List[int]]:
        h, w, _ = face_image.shape
        chose_hand = hands_info.multi_hand_landmarks[hand_index]
        hands_points = [
            [i, int(pt.x * w), int(pt.y * h)]
            for hand in hands_info.multi_hand_landmarks
            for i, pt in enumerate(chose_hand.landmark)
        ]
        return hands_points

    def extract_feature_points(self, hands_points: List[List[int]], feature_indices: dict):
        for feature, indices in feature_indices.items():
            for sub_feature, sub_indices in indices.items():
                self.points[feature][sub_feature] = [hands_points[i][1:] for i in sub_indices]

    def get_hand_points(self, hands_points: List[List[int]]) -> Dict[str, List[List[int]]]:
        feature_indices = {
            'fingers': {
                'distances': [4, 8, 12, 16, 20],
            }
        }
        self.extract_feature_points(hands_points, feature_indices)
        return self.points['fingers']


class HandsDrawer:
    def __init__(self, color: Tuple[int, int, int] = (255, 255, 0)):
        self.mp_draw = mp.solutions.drawing_utils
        self.config_draw = self.mp_draw.DrawingSpec(color=color, thickness=1, circle_radius=1)

    def draw(self, sketch_image: np.ndarray, hands_info: Any):
        for hands in hands_info.multi_hand_landmarks:
            self.mp_draw.draw_landmarks(sketch_image, hands, mp.solutions.hands.HAND_CONNECTIONS,
                                        self.config_draw, self.config_draw)

        return sketch_image


class HandsProcessor:
    def __init__(self):
        self.inference = HandsInference()
        self.extractor = HandsExtractor()
        self.drawer = HandsDrawer()
        self.points: dict = {
            'first_hand': {'distances': []},
            'second_hand': {'distances': []},
        }

    def process(self, hand_image: np.ndarray, sketch_image: np.ndarray, draw: bool = False) -> Tuple[dict, bool, np.ndarray]:
        success, hands_info = self.inference.process(hand_image)
        if not success:
            return self.points, success, sketch_image

        num_hands = self.extractor.count_hands(hands_info)
        if num_hands >= 2:
            first_hand_points = self.extractor.extract_points(hand_image, hands_info, hand_index=0)
            second_hand_points = self.extractor.extract_points(hand_image, hands_info, hand_index=1)
            points = {
                'first_hand': self.extractor.get_hand_points(first_hand_points),
                'second_hand': self.extractor.get_hand_points(second_hand_points),
            }
        else:
            first_hand_points = self.extractor.extract_points(hand_image, hands_info, hand_index=0)
            points = {
                'first_hand': self.extractor.get_hand_points(first_hand_points),
            }

        if draw:
            sketch_image = self.drawer.draw(sketch_image, hands_info)
            return points, success, sketch_image
        return points, success, sketch_image
