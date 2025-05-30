import cv2
import config as cg
import face_recognition as fr
import take_picture as tp
import tkinter as tk

def show_dates(root, button):
    attendance = cg.get_attendance()
    
    tk.Label(root, text="Name", borderwidth=2, relief="solid").grid(row=4, column=1)
    tk.Label(root, text="Time of Entry", borderwidth=2, relief="solid").grid(row=4, column=2)
    tk.Label(root, text="Date", borderwidth=2, relief="solid").grid(row=4, column=3)
    
    row_num = 5

    for i in attendance:
        tk.Label(root, text=i[0], borderwidth=2, relief="solid").grid(row=row_num, column=1)
        tk.Label(root, text=i[1], borderwidth=2, relief="solid").grid(row=row_num, column=2)
        tk.Label(root, text=i[2], borderwidth=2, relief="solid").grid(row=row_num, column=3)
        row_num += 1

    button.config(state="disabled")

def take_attendance():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    cam = cv2.VideoCapture(0)
    
    recognizer.read('trainer.yml')

    #fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    while True:
        ret, frame = cam.read()

        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(grayscale, scaleFactor=1.1, minNeighbors=5)

        cg.initialize_tables()

        for (x, y, w, h) in faces:
            face_region = grayscale[y:y + h, x:x + w]

            label, confidence = recognizer.predict(face_region)

            cv2.putText(frame, f'ID: {label} and Confidence: {confidence}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            if confidence < 35:
                cg.create_attendance()
                cv2.waitKey(200)

        cv2.imshow('Face Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('f'):
            break

    cam.release()
    cv2.destroyAllWindows()

def main():
    root = tk.Tk()
    root.geometry("800x600")

    take_picture = tk.Button(root, text="Take a new Picture", command=tp.take_picture)
    train_model = tk.Button(root, text="Train Model with New Pictures", command=fr.train)
    attendance_window = tk.Button(root, text="Take your attendance", command=take_attendance)
    show_attendance = tk.Button(root, text="Show attendance", command=lambda: show_dates(root, show_attendance))

    take_picture.grid(row=1, column=1, padx=10, pady=5)
    train_model.grid(row=1, column=2, padx=10, pady=5)
    attendance_window.grid(row=1, column=3, padx=10, pady=5)
    show_attendance.grid(row=2, column=2, rowspan=2)

    root.mainloop()

if __name__ == '__main__':
    main()