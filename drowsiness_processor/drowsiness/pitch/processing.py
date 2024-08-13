import time
from typing import Tuple
from abc import ABC, abstractmethod
from drowsiness_processor.drowsiness.processor import DrowsinessProcessor


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
        nose_distance = head_distances['nose_mouth_distance']
        nose_front_distance = head_distances['nose_head_distance']
        nose_point = head_distances['nose_point'][1]
        right_cheek_point = head_distances['right_cheek_point'][1]
        left_cheek_point = head_distances['left_cheek_point'][1]

        if right_cheek_point > nose_point > left_cheek_point:
            self.head_down = True
            self.head_position = 'head down right'
        elif left_cheek_point > nose_point > right_cheek_point:
            self.head_down = True
            self.head_position = 'head down left'
        elif nose_point < right_cheek_point and nose_point < left_cheek_point:
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
            if pitch_duration > 2:
                self.start_time = 0
                self.end_time = 0
                return True, pitch_duration
        return False, 0.0


class PitchCounter:
    def __init__(self):
        self.pitch_count: int = 0
        self.pitch_durations = []

    def increment(self, duration):
        self.pitch_count += 1
        self.pitch_durations.append(f"{self.pitch_count} pitch: {duration} seconds")

    def reset(self):
        self.pitch_count = 0

    def get_durations(self):
        return self.pitch_durations


class PitchEstimator(DrowsinessProcessor):
    def __init__(self):
        self.pitch_detection = PitchDetection()
        self.pitch_counter = PitchCounter()

    def process(self, head_points: dict):
        head_down, head_position = self.pitch_detection.check_head_down(head_points)
        is_pitch, duration_pitch = self.pitch_detection.detect(head_down)
        if is_pitch:
            self.pitch_counter.increment(duration_pitch)

        pitch_count = self.pitch_counter.pitch_count

        if pitch_count > 0:
            return {
                'pitch counter: ': pitch_count,
                'pitch durations: ': self.pitch_counter.get_durations(),
                'pitch report: ': True
            }

        return {
            'pitch counter: ': None,
            'pitch durations: ': self.pitch_counter.get_durations(),
            'pitch report: ': False
        }
