import numpy as np
import base64
import cv2

from drowsiness_processor.extract_points.point_extractor import PointsExtractor
from drowsiness_processor.data_processing.main import PointsProcessing
from drowsiness_processor.drowsiness_features.processing import FeaturesDrowsinessProcessing
from drowsiness_processor.visualization.main import ReportVisualizer
from drowsiness_processor.reports.main import DrowsinessReports


class DrowsinessDetectionSystem:
    def __init__(self):
        self.points_extractor = PointsExtractor()
        self.points_processing = PointsProcessing()
        self.features_processing = FeaturesDrowsinessProcessing()
        self.visualizer = ReportVisualizer()
        self.reports = DrowsinessReports('drowsiness_processor/reports/august/drowsiness_report.csv')
        self.json_report: dict = {}

    def run(self, picture_base64: str):
        # decode base64
        picture_bytes = base64.b64decode(picture_base64)
        # convert bytes to OpenCV image
        picture = cv2.imdecode(np.frombuffer(picture_bytes, np.uint8), cv2.IMREAD_COLOR)
        return self.frame_processing(picture)

    def frame_processing(self, face_image: np.ndarray):
        key_points, control_process, sketch = self.points_extractor.process(face_image)
        if control_process:
            points_processed = self.points_processing.main(key_points)
            drowsiness_features_processed = self.features_processing.main(points_processed)
            sketch = self.visualizer.visualize_all_reports(sketch, drowsiness_features_processed)
            self.reports.main(drowsiness_features_processed)
            self.json_report = self.reports.generate_json_report(drowsiness_features_processed)
        return face_image, sketch, self.json_report
