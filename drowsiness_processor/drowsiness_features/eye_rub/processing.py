import time
from typing import Tuple, Dict, Any
from abc import ABC, abstractmethod
from drowsiness_processor.drowsiness_features.processor import DrowsinessProcessor


class Detector(ABC):
    @abstractmethod
    def detect(self, eyes_distance: dict) -> bool:
        raise NotImplemented


class EyeRubDetection(Detector):
    def __init__(self):
        self.start_time: float = 0
        self.end_time: float = 0
        self.flag: bool = False
        self.eye_rub: bool = False

    def check_eye_rub(self, eye_distance: dict) -> bool:
        distances = [eye_distance[finger] for finger in
                     ['thumb', 'index_finger', 'middle_finger', 'ring_finger', 'little_finger']]
        self.eye_rub = any(distance < 40 for distance in distances)
        return self.eye_rub

    def detect(self, open_mouth: bool) -> Tuple[bool, float]:
        if open_mouth and not self.flag:
            self.start_time = time.time()
            self.flag = True
        elif not open_mouth and self.flag:
            self.end_time = time.time()
            yawn_duration = round(self.end_time - self.start_time, 0)
            self.flag = False
            if yawn_duration > 2:
                self.start_time = 0
                self.end_time = 0
                return True, yawn_duration
        return False, 0.0


class EyeRubCounter:
    def __init__(self):
        self.eye_rub_count: int = 0
        self.eye_rub_durations = []

    def increment(self, duration: float, side: str):
        self.eye_rub_count += 1
        self.eye_rub_durations.append(f"{self.eye_rub_count} {side} eye rub: {duration} seconds")

    def reset(self):
        self.eye_rub_count = 0

    def get_durations(self):
        return self.eye_rub_durations


class ReportGenerator(ABC):
    @abstractmethod
    def generate_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplemented


class EyeRubReportGenerator(ReportGenerator):
    def generate_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        eye_rub_count = data.get("eye_rub_count", 0)
        eye_rub_durations = data.get("eye_rub_durations", [])
        elapsed_time = data.get("elapsed_time", 0)
        eye_rub_report = data.get("eye_rub_report", False)

        return {
            'eye_rub_count_per_5_minutes': eye_rub_count,
            'eye_rub_durations': eye_rub_durations,
            'report_message': f'Counting yawns... {300 - elapsed_time} seconds remaining.',
            'eye_rub_report': eye_rub_report
        }


class EyeRubEstimator(DrowsinessProcessor):
    def __init__(self):
        self.eye_rub_detection = EyeRubDetection()
        self.eye_rub_counter = EyeRubCounter()
        self.eye_rub_report_generator = EyeRubReportGenerator()
        self.start_report = time.time()

    def process(self, hands_points: dict):
        current_time = time.time()
        elapsed_time = round(current_time - self.start_report, 0)

        eye_rub_right = self.eye_rub_detection.check_eye_rub(hands_points['hand_to_right_eye'])
        is_eye_rub_right, duration_eye_rub = self.eye_rub_detection.detect(eye_rub_right)

        eye_rub_left = self.eye_rub_detection.check_eye_rub(hands_points['hand_to_left_eye'])
        is_eye_rub_left, duration_eye_rub = self.eye_rub_detection.detect(eye_rub_left)

        if is_eye_rub_right:
            self.eye_rub_counter.increment(duration_eye_rub, 'right')
        elif is_eye_rub_left:
            self.eye_rub_counter.increment(duration_eye_rub, 'left')

        if elapsed_time >= 300:
            eye_rub_data = {
                "eye_rub_count": self.eye_rub_counter.eye_rub_count,
                "eye_rub_durations": self.eye_rub_counter.get_durations(),
                "elapsed_time": elapsed_time,
                "eye_rub_report": True
            }
            self.eye_rub_counter.reset()
            self.start_report = current_time
            return self.eye_rub_report_generator.generate_report(eye_rub_data)

        return {
            'eye_rub_count_per_5_minutes': f'Counting eye rubs... {300 - elapsed_time} seconds remaining.',
            'eye_rub_report': False
        }
