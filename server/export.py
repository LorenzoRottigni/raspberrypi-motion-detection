import cv2

def export(frames, filename, frame_size, fps=10.0):
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