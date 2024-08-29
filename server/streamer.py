import cv2
import time
from .detection import motion_detection
from .export import export

class Streamer:
    def __init__(self):
        self.recording = False
        self.recording_start_time = None
        self.frames = []

    def stream(self, recording_strategy='live', continuity_threshold=5):
        cap = cv2.VideoCapture(0)
        ret, f1 = cap.read()
        if not ret: return
        f1 = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)

        while True:
            ret, f2 = cap.read()
            if not ret: break
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
                        filename = f"recording_{time.strftime('%Y-%m-%d_%H-%M-%S')}.avi"
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

        cap.release()



