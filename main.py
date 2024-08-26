import cv2

def detect_motion(video_path):
    cap = cv2.VideoCapture(video_path)
    ret, frame1 = cap.read()
    frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

    while True:
        ret, frame2 = cap.read()
        if not ret:
            break
        frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        diff = cv2.absdiff(frame1, frame2)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) > 1000:  # Adjust area threshold as needed
                print("Motion detected!")

        cv2.imshow('frame', thresh)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame1 = frame2

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    video_path = 'path/to/your/video.mp4'  # Replace with your video path
    detect_motion(video_path)