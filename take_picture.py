import cv2
import os

path_to_images = os.getcwd() + '/images'
list_of_images = os.listdir(path_to_images)
cam = cv2.VideoCapture(0)
index = len(list_of_images)

while True:
    ret, frame = cam.read()
    cv2.imshow('Take Image', frame)
    key = cv2.waitKey(1)
    if key == ord('t'):
        filename = os.path.join(path_to_images, f'image{index}.jpg')
        cv2.imwrite(filename, frame)
        index += 1
    elif key == ord('f'):
        break

cam.release()
cv2.destroyAllWindows()