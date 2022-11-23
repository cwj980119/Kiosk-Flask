import dlib,cv2
import numpy as np

def check():
    detector = dlib.get_frontal_face_detector()
    frame = cv2.imread('./image/check.jpg', 1)
    face = detector(frame)
    return len(face)

def origincheck():
    detector = dlib.get_frontal_face_detector()
    frame = cv2.imread('./image/check.jpg', 1)
    face = detector(frame)
    return len(face)