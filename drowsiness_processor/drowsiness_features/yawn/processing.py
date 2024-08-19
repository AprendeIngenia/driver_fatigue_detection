import time
from typing import Tuple, Dict, Any
from abc import ABC, abstractmethod
from drowsiness_processor.drowsiness_features.processor import DrowsinessProcessor


class Detector(ABC):
    @abstractmethod
    def detect(self, mouth_distance: dict) -> bool:
        raise NotImplemented


class YawnDetection(Detector):
    def __init__(self):
        self.start_time: float = 0
        self.end_time: float = 0
        self.flag: bool = False
        self.open_mouth: bool = False

    def check_open_mouth(self, mouth_distances: dict) -> bool:
        lips_distance = mouth_distances['lips_distance']
        chin_distance = mouth_distances['chin_distance']

        if lips_distance > chin_distance:
            self.open_mouth = True
        elif lips_distance < chin_distance:
            self.open_mouth = False
        return self.open_mouth

    def detect(self, open_mouth: bool) -> Tuple[bool, float]:
        if open_mouth and not self.flag:
            self.start_time = time.time()
            self.flag = True
        elif not open_mouth and self.flag:
            self.end_time = time.time()
            yawn_duration = round(self.end_time - self.start_time, 0)
            self.flag = False
            if yawn_duration > 4:
                self.start_time = 0
                self.end_time = 0
                return True, yawn_duration
        return False, 0.0


class YawnCounter:
    def __init__(self):
        self.yawn_count: int = 0
        self.yawn_durations = []

    def increment(self, duration: float):
        self.yawn_count += 1
        self.yawn_durations.append(f"{self.yawn_count} yawn: {duration} seconds")

    def reset(self):
        self.yawn_count = 0

    def get_durations(self):
        return self.yawn_durations


class ReportGenerator(ABC):
    @abstractmethod
    def generate_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplemented


class YawnReportGenerator(ReportGenerator):
    def generate_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        yawn_count = data.get("yawn_count", 0)
        yawn_durations = data.get("yawn_durations", [])
        elapsed_time = data.get("elapsed_time", 0)
        yawn_report = data.get("yawn_report", False)

        return {
            'yawn_count': yawn_count,
            'yawn_durations': yawn_durations,
            'report_message': f'Counting yawns... {180 - elapsed_time} seconds remaining.',
            'yawn_report': yawn_report
        }


class YawnEstimator(DrowsinessProcessor):
    def __init__(self):
        self.yawn_detection = YawnDetection()
        self.yawn_counter = YawnCounter()
        self.yawn_report_generator = YawnReportGenerator()
        self.start_report = time.time()

    def process(self, mouth_points: dict):
        current_time = time.time()
        elapsed_time = round(current_time - self.start_report, 0)

        open_mouth = self.yawn_detection.check_open_mouth(mouth_points)
        is_yawn, duration_yawn = self.yawn_detection.detect(open_mouth)
        if is_yawn:
            self.yawn_counter.increment(duration_yawn)

        if elapsed_time >= 180:
            yawn_data = {
                "yawn_count": self.yawn_counter.yawn_count,
                "yawn_durations": self.yawn_counter.get_durations(),
                "elapsed_time": elapsed_time,
                "yawn_report": True
            }
            self.yawn_counter.reset()
            self.start_report = current_time
            return self.yawn_report_generator.generate_report(yawn_data)

        return {
            'yawn_count': f'Counting yawns... {180 - elapsed_time} seconds remaining.',
            'yawn_report': False
        }
