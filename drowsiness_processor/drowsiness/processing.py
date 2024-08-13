from drowsiness_processor.drowsiness.processor import DrowsinessProcessor
from drowsiness_processor.drowsiness.eye_rub.processing import EyeRubEstimator
from drowsiness_processor.drowsiness.flicker_and_microsleep.processing import FlickerEstimator
from drowsiness_processor.drowsiness.pitch.processing import PitchEstimator
from drowsiness_processor.drowsiness.yawn.processing import YawnEstimator


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
        self.processed_feature['flicker and micro sleep'] = (self.features_drowsiness['flicker and micro sleep'].process
                                                             (distances.get('eyes', {})))

        #if 'first_hand' in distances:
        #    self.processed_feature['eye rub'] = (self.features_drowsiness['eye rub'].process(distances['first_hand']))

        #if 'second_hand' in distances:
        #    self.processed_feature['eye rub'] = (self.features_drowsiness['eye rub'].process(distances['second_hand']))

        self.processed_feature['pitch'] = self.features_drowsiness['pitch'].process(distances.get('head', {}))
        self.processed_feature['yawn'] = self.features_drowsiness['yawn'].process(distances.get('mouth', {}))
        print(self.processed_feature)

        return self.processed_feature
