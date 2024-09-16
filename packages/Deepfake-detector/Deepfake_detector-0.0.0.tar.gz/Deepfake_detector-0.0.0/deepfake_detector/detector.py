import os
import cv2
import numpy as np
import tensorflow as tf
import requests
from tensorflow.keras.models import load_model
from zipfile import ZipFile

# Define constants
FRAME_SIZE = (224, 224)
MODEL_URL = 'https://drive.google.com/uc?export=download&id=1X0RjFENxbMVT9Zvvzsu43smGq_wFiVIC'
MODEL_PATH = os.path.join(os.path.expanduser('~'), '.deepfake_detector', 'deepfake.h5')

# Ensure the model is downloaded if not present
def download_model():
    if not os.path.exists(MODEL_PATH):
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        print("Downloading model...")

        response = requests.get(MODEL_URL, stream=True)
        with open(MODEL_PATH, 'wb') as file:
            file.write(response.content)

        print("Model downloaded successfully.")

# Load the model
def load_deepfake_model():
    download_model()
    model = load_model(MODEL_PATH)
    return model

# Preprocessing function for frames
def preprocess_frame(frame):
    frame = cv2.resize(frame, FRAME_SIZE)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = tf.keras.applications.efficientnet.preprocess_input(frame)
    return np.expand_dims(frame, axis=0)

# Predict a face using the model
def predict_face(model, face, threshold):
    preprocessed_face = preprocess_frame(face)
    pred = model.predict(preprocessed_face)
    return pred[0][0] > threshold

# Predict from video source (live webcam or video file)
def predict_video(source=0, threshold=0.5):
    model = load_deepfake_model()
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(source)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face = frame[y:y + h, x:x + w]
            is_fake = predict_face(model, face, threshold)
            label = 'FAKE' if is_fake else 'REAL'
            color = (0, 0, 255) if is_fake else (0, 255, 0)

            cv2.putText(frame, f'{label}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        cv2.imshow('Deepfake Detector', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Predict from a single image
def predict_image(image_path, threshold=0.5):
    model = load_deepfake_model()
    img = cv2.imread(image_path)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) == 0:
        raise ValueError("No face detected in the image.")

    (x, y, w, h) = max(faces, key=lambda rect: rect[2] * rect[3])
    face = img[y:y + h, x:x + w]

    is_fake = predict_face(model, face, threshold)
    label = 'FAKE' if is_fake else 'REAL'
    
    cv2.putText(img, f'{label}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return img
