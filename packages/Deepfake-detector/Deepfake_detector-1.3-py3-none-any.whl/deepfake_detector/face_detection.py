import cv2
import numpy as np
import tensorflow as tf
from .utils import download_model, preprocess_frame

# Download and load the model
model_path = download_model()
model = tf.keras.models.load_model(model_path)

# Video prediction function
def live_video_prediction(source=0, threshold=0.4):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(source)
        
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face = frame[y:y+h, x:x+w]
            prediction = predict_face(face)

            label = 'FAKE' if prediction > threshold else 'REAL'
            color = (0, 0, 255) if label == 'FAKE' else (0, 255, 0)
            cv2.putText(frame, f'{label}: {prediction:.2f}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

        cv2.imshow('Live Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Image prediction function
def image_prediction(image_path, threshold=0.4):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        raise ValueError("No face detected in the image.")

    (x, y, w, h) = max(faces, key=lambda rect: rect[2] * rect[3])
    face = img[y:y+h, x:x+w]
    prediction = predict_face(face)

    label = 'FAKE' if prediction > threshold else 'REAL'
    color = (0, 0, 255) if label == 'FAKE' else (0, 255, 0)
    cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)

    cv2.putText(img, f'{label}: {prediction:.2f}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.imshow('Image Prediction', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def predict_face(face):
    preprocessed_face = preprocess_frame(face)
    pred = model.predict(preprocessed_face)
    return pred[0][0]
