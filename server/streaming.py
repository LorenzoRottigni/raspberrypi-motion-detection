import cv2
import time
from .detection import motion_detection

def save_recording(frames, filename, frame_size, fps=10.0):
    writer = cv2.VideoWriter(
        filename=filename,
        apiPreference=cv2.CAP_FFMPEG,
        fourcc=cv2.VideoWriter_fourcc(*"XVID"),
        fps=fps,
        frameSize=frame_size,
        isColor=False
    )
    for frame in frames:
        writer.write(frame)
    writer.release()

def generate_frames(
        recording_strategy = 'live',
        continuity_threshold = 5
    ):
    cap = cv2.VideoCapture(0)
    ret, f1 = cap.read()
    if not ret:
        cap.release()
        return

    f1 = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)
    
    recording = False
    recording_start_time = None
    frames = []

    while True:
        ret, f2 = cap.read()
        if not ret:
            break

        f2 = cv2.cvtColor(f2, cv2.COLOR_BGR2GRAY)
        strategy_satisfied = False

        strategy_satisfied, f2 = motion_detection(f1, f2) if recording_strategy == 'motion_detection' else (False, f2)

        if strategy_satisfied:
            if not recording:
                recording = True
                frames = []
                print("Starting new recording.")
            recording_start_time = time.time()
            frames.append(f2)
        elif recording and (time.time() - recording_start_time) < continuity_threshold:
            frames.append(f2)
        else:
            if recording:
                recording = False
                if frames:
                    filename = f"recording_{time.strftime('%Y-%m-%d_%H-%M-%S')}.avi"
                    save_recording(frames, filename, (f2.shape[1], f2.shape[0]))
                    print(f"Recording saved to '{filename}'.")
                frames = []
                recording_start_time = None

        # Convert frame to JPEG format for streaming
        ret, buffer = cv2.imencode('.jpg', f2)
        if not ret:
            continue

        frame_bytes = buffer.tobytes()

        # Yield the frame as part of the stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        f1 = f2

    cap.release()
