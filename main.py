import cv2
import time

def motion_detection(f1, f2):
    diff = cv2.absdiff(f1, f2)
    _, threshold = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > 1000:
            return True, contour
    return False, None

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

def record():
    cap = cv2.VideoCapture(0)
    ret, f1 = cap.read()
    if not ret:
        return

    f1 = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)
    
    recording = False
    recording_start_time = None
    continuity_threshold = 5
    frames = []

    while True:
        ret, f2 = cap.read()
        if not ret:
            break

        f2 = cv2.cvtColor(f2, cv2.COLOR_BGR2GRAY)
        frame_width = f2.shape[1]
        frame_height = f2.shape[0]

        motion_detected, contour = motion_detection(f1, f2)

        if motion_detected:
            if not recording:
                recording = True
                frames = []  # Start a new recording
            recording_start_time = time.time()
            frames.append(f2)
        elif recording and (time.time() - recording_start_time) < continuity_threshold:
            frames.append(f2)
        else:
            if recording:
                recording = False
                # Save recording upon 5s of inactivity after motion
                if frames:
                    filename = f"recording_{time.strftime('%Y-%m-%d_%H-%M-%S')}.avi"
                    save_recording(frames, filename, (frame_width, frame_height))
                    print(f"Recording saved to '{filename}'")
                frames = []
                recording_start_time = None

        if recording and contour is not None:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(f2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('Frame (Recording)', f2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        f1 = f2

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    record()
