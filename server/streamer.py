import cv2
import time
from .detection import motion_detection
from .export import export
import numpy as np
class Streamer:
    def __init__(self):
        self.recording = False
        self.recording_start_time = None
        self.frames = []
        self.capture = False
        self.stream = None
        self.cap = None
        self.running = None

    def boot(self, strategy, continuity_threshold):
        if (self.stream): self.close_stream()
        self.stream = self.stream_generator(
            strategy,
            continuity_threshold
        )

    def get_fallback_frame(self):
        frame_width, frame_height = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        f = np.zeros((int(frame_height), int(frame_width), 1), dtype=np.uint8)
        cv2.putText(f, "Failed to capture frame.", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        return f

    def stream_generator(self, recording_strategy='live', continuity_threshold=5):
        print(f"Starting a new video stream ({recording_strategy})...")
        self.cap = cv2.VideoCapture(0)
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        ret, f1 = self.cap.read()
        if not ret: return
        f1 = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)
        self.capture = True

        while self.capture:
            self.running = True
            ret, f2 = self.cap.read()
            if not ret: f2 = self.get_fallback_frame() # break
            f2 = cv2.cvtColor(f2, cv2.COLOR_BGR2GRAY)
            strategy_satisfied = False
            strategy_satisfied, f2 = motion_detection(f1, f2) if recording_strategy == 'motion_detection' else (False, f2)

            if strategy_satisfied:
                if not self.recording:
                    self.recording = True
                    self.frames = []
                    print("Starting new recording.")
                    self.recording_start_time = time.time()
                self.frames.append(f2)
            elif self.recording and (time.time() - self.recording_start_time) < continuity_threshold:
                self.frames.append(f2)
            else:
                if self.recording:
                    self.recording = False
                    if self.frames:
                        filename = f"data/recording_{time.strftime('%Y-%m-%d_%H-%M-%S')}.avi"
                        try:
                            export(self.frames, filename, (f2.shape[1], f2.shape[0]))
                            print(f"Recording saved to '{filename}'.")
                        except Exception as e:
                            print(f"Error saving recording: {e}")
                    self.frames = []
                    self.recording_start_time = None

            ret, buffer = cv2.imencode('.jpg', f2)
            if not ret: continue

            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n') 
            f1 = f2

        self.close_stream()

    def close_stream(self):
        print("Closing stream...")
        if self.stream:
            try:
                # print("Consuming previous stream generator...")
                # list(self.stream)
                self.stream = None

            except Exception as e:
                print(f"Error while closing the stream: {e}.")
        self.capture = False
        if self.cap.isOpened():
            self.cap.release()



