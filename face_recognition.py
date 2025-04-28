import cv2
import numpy as np
import os

def get_images_from_folder():
    images_dir = os.getcwd() + '/images'
    image_names = os.listdir(images_dir)
    images = []
    for i in image_names:
        images.append(cv2.imread('images/' + i))

    return images

def train():
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    faces = []
    labels = []

    images = get_images_from_folder()

    index = 1

    for img in images:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces.append(gray)
        labels.append(index)

    recognizer.train(faces, np.array(labels))

    recognizer.save('trainer.yml')