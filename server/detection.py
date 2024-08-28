import cv2

def motion_detection(f1, f2):
    diff = cv2.absdiff(f1, f2)
    _, threshold = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > 1000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(f2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            return True, f2
    return False, f2
