import time
from typing import Tuple, Dict, Any
from abc import ABC, abstractmethod
from drowsiness_processor.drowsiness_features.processor import DrowsinessProcessor


class Detector(ABC):
    @abstractmethod
    def detect(self, eyes_distance: dict) -> bool:
        raise NotImplemented


class FlickerDetection(Detector):
    def __init__(self):
        self.is_flicker: bool = False

    def detect(self, eyes_distance: dict) -> bool:
        right_eyelid_upper = eyes_distance['right_upper_eyelid_distance']
        right_eyelid_lower = eyes_distance['right_lower_eyelid_distance']
        left_eyelid_upper = eyes_distance['left_upper_eyelid_distance']
        left_eyelid_lower = eyes_distance['left_lower_eyelid_distance']

        if right_eyelid_upper < right_eyelid_lower and left_eyelid_upper < left_eyelid_lower and not self.is_flicker:
            self.is_flicker = True
            return True
        elif right_eyelid_upper > right_eyelid_lower and left_eyelid_upper > left_eyelid_lower and self.is_flicker:
            self.is_flicker = False
        return False


class MicroSleepDetection(Detector):
    def __init__(self):
        self.start_time: float = 0
        self.end_time: float = 0
        self.flag: bool = False
        self.close_eyes: bool = False

    def closed_eyes(self, eyes_distance: dict) -> bool:
        right_eyelid_upper = eyes_distance['right_upper_eyelid_distance']
        right_eyelid_lower = eyes_distance['right_lower_eyelid_distance']
        left_eyelid_upper = eyes_distance['left_upper_eyelid_distance']
        left_eyelid_lower = eyes_distance['left_lower_eyelid_distance']

        if right_eyelid_upper < right_eyelid_lower and left_eyelid_upper < left_eyelid_lower and not self.close_eyes:
            self.close_eyes = True
        elif right_eyelid_upper > right_eyelid_lower and left_eyelid_upper > left_eyelid_lower and self.close_eyes:
            self.close_eyes = False
        return self.close_eyes

    def detect(self, is_eyes_closed: bool) -> Tuple[bool, float]:
        if is_eyes_closed and not self.flag:
            self.start_time = time.time()
            self.flag = True
        elif not is_eyes_closed and self.flag:
            self.end_time = time.time()
            flicker_duration = round(self.end_time - self.start_time, 0)
            self.flag = False
            if flicker_duration >= 2:
                self.start_time = 0
                self.end_time = 0
                return True, flicker_duration
        return False, 0.0


class FlickerCounter:
    def __init__(self):
        self.flicker_count: int = 0

    def increment(self):
        self.flicker_count += 1

    def reset(self):
        self.flicker_count = 0


class MicroSleepCounter:
    def __init__(self):
        self.micro_sleep_count: int = 0
        self.micro_sleep_durations = []

    def increment(self, duration: float):
        self.micro_sleep_count += 1
        self.micro_sleep_durations.append(f"{self.micro_sleep_count} micro sleep: {duration} seconds")

    def reset(self):
        self.micro_sleep_count = 0

    def get_durations(self):
        return self.micro_sleep_durations


class ReportGenerator(ABC):
    @abstractmethod
    def generate_report(self, data: dict[str, bool | int | list]) -> Dict[str, Any]:
        raise NotImplemented


class FlickerReportGenerator(ReportGenerator):
    def generate_report(self, data: dict[str, bool | int | list]) -> Dict[str, Any]:
        flicker_count = data.get("flicker_count", 0)
        elapsed_time = data.get("elapsed_time", 0)
        flicker_report = data.get("flicker_report", False)
        micro_sleep_report = data.get("micro_sleep_Report", False)

        return {
            'flicker_count': flicker_count,
            'report_message': f'Counting flickers... {60 - elapsed_time} seconds remaining.',
            'flicker_report': flicker_report,
            'micro_sleep_report': micro_sleep_report
        }


class MicroSleepReportGenerator(ReportGenerator):
    def generate_report(self, data: dict[str, bool | int | list]) -> Dict[str, Any]:
        micro_sleep_count = data.get("micro_sleep_count", 0)
        micro_sleep_durations = data.get("micro_sleep_durations", [])
        micro_sleep_report = data.get("micro_sleep_report", False)
        flicker_report = data.get("flicker_report", False)

        return {
            'micro_sleep_count': micro_sleep_count,
            'micro_sleep_durations': micro_sleep_durations,
            'micro_sleep_report': micro_sleep_report,
            'flicker_report': flicker_report
        }


class FlickerEstimator(DrowsinessProcessor):
    def __init__(self):
        self.flicker_detector = FlickerDetection()
        self.micro_sleep_detector = MicroSleepDetection()
        self.flicker_counter = FlickerCounter()
        self.micro_sleep_counter = MicroSleepCounter()
        self.flicker_report_generator = FlickerReportGenerator()
        self.micro_sleep_report_generator = MicroSleepReportGenerator()
        self.start_report = time.time()

    def process(self, eyes_distance: dict):
        current_time = time.time()
        elapsed_time = round(current_time - self.start_report, 0)

        is_flicker = self.flicker_detector.detect(eyes_distance)
        if is_flicker:
            self.flicker_counter.increment()

        closed_eyes = self.micro_sleep_detector.closed_eyes(eyes_distance)
        is_micro_sleep, duration_micro_sleep = self.micro_sleep_detector.detect(closed_eyes)
        if is_micro_sleep:
            self.micro_sleep_counter.increment(duration_micro_sleep)

        micro_sleep = self.micro_sleep_counter.micro_sleep_count

        if elapsed_time >= 60:
            flicker_data = {
                "flicker_count": self.flicker_counter.flicker_count,
                "elapsed_time": elapsed_time,
                "flicker_report": True,
                "micro_sleep_report": False,
            }
            self.flicker_counter.reset()
            self.start_report = current_time
            return self.flicker_report_generator.generate_report(flicker_data)

        if is_micro_sleep:
            micro_sleep_data = {
                "micro_sleep_count": self.micro_sleep_counter.micro_sleep_count,
                "micro_sleep_durations": self.micro_sleep_counter.get_durations(),
                "micro_sleep_report": True,
                "flicker_report": False
            }
            return self.micro_sleep_report_generator.generate_report(micro_sleep_data)

        return {
            'flicker_count': f'Counting flickers... {60 - elapsed_time} seconds remaining.',
            'flicker_report': False,
            'micro_sleep_report': False
        }
