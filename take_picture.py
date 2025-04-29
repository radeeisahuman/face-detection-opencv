import cv2
import os
import numpy as np

path_to_images = os.getcwd() + '/images'
list_of_images = os.listdir(path_to_images)
cam = cv2.VideoCapture(0)
index = len(list_of_images)

while True:
    ret, frame = cam.read()
    flash = 255 * np.ones_like(frame, dtype=np.uint8)
    cv2.imshow('Take Image', frame)
    key = cv2.waitKey(1)
    if key == ord('t'):
        filename = os.path.join(path_to_images, f'image{index}.jpg')
        cv2.imshow('Take Image', flash)
        cv2.waitKey(100)
        cv2.imwrite(filename, frame)
        index += 1
    elif key == ord('f'):
        break

cam.release()
cv2.destroyAllWindows()