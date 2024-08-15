from drowsiness_processor.drowsiness_features.processor import DrowsinessProcessor
from drowsiness_processor.drowsiness_features.eye_rub.processing import EyeRubEstimator
from drowsiness_processor.drowsiness_features.flicker_and_microsleep.processing import FlickerEstimator
from drowsiness_processor.drowsiness_features.pitch.processing import PitchEstimator
from drowsiness_processor.drowsiness_features.yawn.processing import YawnEstimator


class FeaturesDrowsinessProcessing:
    def __init__(self):
        self.features_drowsiness: dict[str, DrowsinessProcessor] = {
            'eye rub': EyeRubEstimator(),
            'flicker and micro sleep': FlickerEstimator(),
            'pitch': PitchEstimator(),
            'yawn': YawnEstimator(),
        }
        self.processed_feature: dict = {}

    def main(self, distances: dict):
        self.processed_feature = {}
        if 'first hand' in distances:
            self.processed_feature['eye rub first hand'] = (self.features_drowsiness['eye rub'].process(distances['first hand']))

        if 'second hand' in distances:
            self.processed_feature['eye rub second hand'] = (self.features_drowsiness['eye rub'].process(distances['second hand']))

        self.processed_feature['flicker and micro sleep'] = (self.features_drowsiness['flicker and micro sleep'].process
                                                             (distances.get('eyes', {})))
        self.processed_feature['pitch'] = self.features_drowsiness['pitch'].process(distances.get('head', {}))
        self.processed_feature['yawn'] = self.features_drowsiness['yawn'].process(distances.get('mouth', {}))
        return self.processed_feature
