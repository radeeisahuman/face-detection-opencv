import cv2
import config

def main():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    cam = cv2.VideoCapture(0)

    recognizer.read('trainer.yml')

    #fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    while True:
        ret, frame = cam.read()

        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(grayscale, scaleFactor=1.1, minNeighbors=5)

        config.initialize_tables()

        for (x, y, w, h) in faces:
            face_region = grayscale[y:y + h, x:x + w]

            label, confidence = recognizer.predict(face_region)

            cv2.putText(frame, f'ID: {label} and Confidence: {confidence}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            if confidence > 70:
                config.create_attendance()

        cv2.imshow('Face Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('f'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()