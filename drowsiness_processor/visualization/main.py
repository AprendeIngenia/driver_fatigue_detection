import numpy as np
import cv2
import time
from typing import Tuple


class ReportVisualizer:
    def __init__(self):
        self.coordinates = {
            'eye_rub_first_hand': (10, 20),
            'eye_rub_second_hand': (10, 100),
            'flicker': (10, 180),
            'micro_sleep': (10, 260),
            'pitch': (10, 340),
            'yawn': (10, 420),
        }
        self.visualize_reports = {
            'eye_rub_first_hand': {'report': False, 'count': 0, 'durations': []},
            'eye_rub_second_hand': {'report': False, 'count': 0, 'durations': []},
            'flicker': {'report': False, 'count': 0},
            'micro_sleep': {'report': False, 'count': 0, 'durations': []},
            'pitch': {'report': False, 'count': 0, 'durations': []},
            'yawn': {'report': False, 'count': 0, 'durations': []}
        }
        self.times = {
            'eye_rub_first_hand': time.time(),
            'eye_rub_second_hand': time.time(),
            'flicker': time.time(),
            'yawn': time.time()
        }
        self.warnings = {
            'eye_rub_first_hand': 10,
            'eye_rub_second_hand': 10,
            'micro_sleep': 1,
            'pitch': 1,
            'flicker': 20,
            'yawn': 10
        }

        self.initial_position: int = 20
        self.spacing: int = 80
        self.margin: int = 40

    def draw_rectangle(self, sketch: np.ndarray, top_left: Tuple[int, int], bottom_right: Tuple[int, int],
                       color: Tuple[int, int, int]):
        cv2.rectangle(sketch, top_left, bottom_right, color, 2)

    def get_color(self, report_status: str) -> Tuple[int, int, int]:
        if report_status == 'waiting':
            return 180, 180, 180
        elif report_status == 'warning':
            return 0, 255, 255
        elif report_status == 'alarm':
            return 0, 0, 255
        elif report_status == 'normal':
            return 0, 255, 0

    def draw_report_text(self, sketch: np.ndarray, text: str, position: Tuple[int, int], color: Tuple[int, int, int]):
        cv2.putText(sketch, text, position, cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)

    def draw_warnings_general(self, sketch: np.ndarray, feature: str):
        position = self.coordinates[feature]
        color = self.get_color('waiting')
        if feature == 'micro_sleep' or feature == 'pitch':
            if feature == 'micro_sleep':
                self.draw_report_text(sketch,
                                      f"evaluating: {feature.replace('_', ' ')}: stay alert",
                                      position, color)

            if feature == 'pitch':
                self.draw_report_text(sketch,
                                      f"evaluating: {feature.replace('_', ' ')}: stay alert",
                                      position, color)
        else:
            current_time = time.time()
            start_time_feature = self.times[feature]
            elapsed_time = round(current_time - start_time_feature, 0)

            if feature == 'eye_rub_first_hand' or feature == 'eye_rub_second_hand':
                self.draw_report_text(sketch,
                                      f"counting: {feature.replace('_', ' ')}: {300 - elapsed_time} seconds remaining",
                                      position, color)

            if feature == 'flicker':
                self.draw_report_text(sketch,
                                      f"counting: {feature.replace('_', ' ')}: {60 - elapsed_time} seconds remaining",
                                      position, color)

            if feature == 'yawn':
                self.draw_report_text(sketch,
                                      f"counting: {feature.replace('_', ' ')}: {180 - elapsed_time} seconds remaining",
                                      position, color)

    def draw_warnings_report(self, sketch: np.ndarray, feature: str):
        position = self.coordinates[feature]
        feature_count = self.visualize_reports[feature]['count']
        warning_threshold = self.warnings[feature]

        if feature == 'micro_sleep' or feature == 'pitch':
            if feature_count >= warning_threshold:
                color = self.get_color('alarm')
        else:
            if feature_count > warning_threshold:
                color = self.get_color('warning')
            else:
                color = self.get_color('normal')

        self.draw_report_text(sketch, f"{feature.replace('_', ' ')} {feature}: {feature_count}", position, color)

        if feature == 'flicker':
            text = f"{feature.replace('_', ' ')} {feature}: {feature_count}"
            text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
            text_width, text_height = text_size
            top_left = (position[0] - 10, position[1] - 20)
            bottom_right = (position[0] + text_width + 20, position[1] + text_height + 20)
            self.draw_rectangle(sketch, top_left, bottom_right, color)
            self.update_coordinates(feature, (10, bottom_right[1]))

        if feature != 'flicker':
            feature_durations = self.visualize_reports[feature]['durations']

            y_offset = position[1] + 30
            for i, duration in enumerate(feature_durations):
                self.draw_report_text(sketch, f"#{i + 1}: {duration} sec", (position[0], y_offset), color)
                y_offset += 20

                text = f"#{i + 1}: {duration} sec"

                text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
                text_width, text_height = text_size
                top_left = (position[0] - 10, position[1] - 20)
                bottom_right = (position[0] + text_width + 20, position[1] + text_height + 20 * (len(feature_durations) + 1))
                self.draw_rectangle(sketch, top_left, bottom_right, color)
                self.update_coordinates(feature, (10, bottom_right[1]))

    def update_coordinates(self, feature: str, new_coordinates: tuple[int, int]):
        keys = list(self.coordinates.keys())
        coordinates = list(self.coordinates.values())
        position = keys.index(feature)
        x, y = new_coordinates
        y = y + self.margin
        if position == 5:
            pass
        else:
            coordinates[position+1] = (x, y)
            self.coordinates = dict(zip(keys, coordinates))

    def update_report(self, feature: str, data: dict):
        base_feature = feature.replace('_first_hand', '').replace('_second_hand', '')
        report = data[f'{base_feature}_report']

        if report:
            counter = data[f'{base_feature}_count']
            self.visualize_reports[feature]['report'] = report
            self.visualize_reports[feature]['count'] = counter

        if feature != 'flicker':
            if report:
                durations = data[f'{base_feature}_durations']
                self.visualize_reports[feature]['durations'] = durations

    def visualize_all_reports(self, sketch: np.ndarray, report_data: dict):
        # first hand
        self.update_report('eye_rub_first_hand', report_data['eye_rub_first_hand'])
        if self.visualize_reports['eye_rub_first_hand']['report']:
            self.draw_warnings_report(sketch, 'eye_rub_first_hand')
        else:
            self.draw_warnings_general(sketch, 'eye_rub_first_hand')

        # second hand
        self.update_report('eye_rub_second_hand', report_data['eye_rub_second_hand'])
        if self.visualize_reports['eye_rub_second_hand']['report']:
            self.draw_warnings_report(sketch, 'eye_rub_second_hand')
        else:
            self.draw_warnings_general(sketch, 'eye_rub_second_hand')

        # flicker
        self.update_report('flicker', report_data['flicker_and_micro_sleep'])
        if self.visualize_reports['flicker']['report']:
            self.draw_warnings_report(sketch, 'flicker')
        else:
            self.draw_warnings_general(sketch, 'flicker')

        # micro sleep
        self.update_report('micro_sleep', report_data['flicker_and_micro_sleep'])
        if self.visualize_reports['micro_sleep']['report']:
            self.draw_warnings_report(sketch, 'micro_sleep')
        else:
            self.draw_warnings_general(sketch, 'micro_sleep')

        # pitch
        self.update_report('pitch', report_data['pitch'])
        if self.visualize_reports['pitch']['report']:
            self.draw_warnings_report(sketch, 'pitch')
        else:
            self.draw_warnings_general(sketch, 'pitch')

        # yawn
        self.update_report('yawn', report_data['yawn'])
        if self.visualize_reports['yawn']['report']:
            self.draw_warnings_report(sketch, 'yawn')
        else:
            self.draw_warnings_general(sketch, 'yawn')
        return sketch
