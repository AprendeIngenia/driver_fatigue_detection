import os
import sys
import cv2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from drowsiness_processor.main import DrowsinessDetectionSystem
from camera import Camera


class VideoStream:
    def __init__(self, cam: Camera, drowsiness_detection_system: DrowsinessDetectionSystem):
        self.camera = cam
        self.drowsiness_detection_system = drowsiness_detection_system

    def run(self):
        while True:
            ret, frame = self.camera.read()
            if ret:
                frame, sketch, json_report = self.drowsiness_detection_system.frame_processing(frame)
                print(json_report)
                cv2.imshow('Emotion Recognition', frame)
                cv2.imshow('3D sketch image', sketch)
                t = cv2.waitKey(5)
                if t == 27:
                    break

            else:
                Exception(f"No cam connected")
        self.camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    #camera = Camera(0, 1280, 720)
    camera = Camera("examples/video_example.mp4", 1280, 720)
    emotion_recognition_system = DrowsinessDetectionSystem()
    video_stream = VideoStream(camera, emotion_recognition_system)
    video_stream.run()


