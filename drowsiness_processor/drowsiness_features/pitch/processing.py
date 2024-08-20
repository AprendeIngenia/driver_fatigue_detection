import time
from typing import Tuple, Dict, Any
from abc import ABC, abstractmethod
from drowsiness_processor.drowsiness_features.processor import DrowsinessProcessor


class Detector(ABC):
    @abstractmethod
    def detect(self, head_distances: dict) -> Tuple[bool, str]:
        raise NotImplemented


class PitchDetection(Detector):
    def __init__(self):
        self.start_time: float = 0
        self.end_time: float = 0
        self.flag: bool = False
        self.head_down: bool = False
        self.head_position: str = ''

    def check_head_down(self, head_distances: dict) -> Tuple[bool, str]:
        nose_mouth_distance = head_distances['nose_mouth_distance']
        nose_front_distance = head_distances['nose_head_distance']
        nose_point = head_distances['nose_point'][1]
        right_cheek_point = head_distances['right_cheek_point'][1]
        left_cheek_point = head_distances['left_cheek_point'][1]

        if right_cheek_point > nose_point > left_cheek_point and nose_mouth_distance < nose_front_distance:
            self.head_down = True
            self.head_position = 'head down right'
        elif left_cheek_point > nose_point > right_cheek_point and nose_mouth_distance < nose_front_distance:
            self.head_down = True
            self.head_position = 'head down left'
        elif nose_point < right_cheek_point and nose_point < left_cheek_point and nose_mouth_distance > nose_front_distance:
            self.head_down = False
            self.head_position = 'head up'
        return self.head_down, self.head_position

    def detect(self, head_down: bool) -> Tuple[bool, float]:
        if head_down and not self.flag:
            self.start_time = time.time()
            self.flag = True
        elif not head_down and self.flag:
            self.end_time = time.time()
            pitch_duration = round(self.end_time - self.start_time, 0)
            self.flag = False
            if pitch_duration >= 3.0:
                self.start_time = 0
                self.end_time = 0
                return True, pitch_duration
        return False, 0.0


class PitchCounter:
    def __init__(self):
        self.pitch_count: int = 0
        self.pitch_durations = []

    def increment(self, duration: float):
        self.pitch_count += 1
        self.pitch_durations.append(f"{self.pitch_count} pitch: {duration} seconds")

    def reset(self):
        self.pitch_count = 0

    def get_durations(self):
        return self.pitch_durations


class ReportGenerator(ABC):
    @abstractmethod
    def generate_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplemented


class PitchReportGenerator(ReportGenerator):
    def generate_report(self, data: Dict[str, Any]) -> dict[str, Any]:
        pitch_count = data.get("pitch_count", 0)
        pitch_durations = data.get("pitch_durations", [])
        head_down = data.get("head_down", False)
        pitch_report = data.get("pitch_report", False)

        return {
            'pitch_count': pitch_count,
            'pitch_durations': pitch_durations,
            'head_down': head_down,
            'pitch_report': pitch_report
        }


class PitchEstimator(DrowsinessProcessor):
    def __init__(self):
        self.pitch_detection = PitchDetection()
        self.pitch_counter = PitchCounter()
        self.pitch_report_generator = PitchReportGenerator()

    def process(self, head_points: dict):
        head_down, head_position = self.pitch_detection.check_head_down(head_points)
        is_pitch, duration_pitch = self.pitch_detection.detect(head_down)
        if is_pitch:
            self.pitch_counter.increment(duration_pitch)

        if is_pitch:
            pitch_data = {
                "pitch_count": self.pitch_counter.pitch_count,
                "pitch_durations": self.pitch_counter.get_durations(),
                "head_down": head_down,
                "pitch_report": True
            }

            return self.pitch_report_generator.generate_report(pitch_data)

        return {
            'pitch_count': f'Counting pitches...',
            'pitch_report': False,
            'head_down': head_down
        }
