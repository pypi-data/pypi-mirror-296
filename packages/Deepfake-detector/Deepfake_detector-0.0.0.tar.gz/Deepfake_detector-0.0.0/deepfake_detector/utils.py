import cv2
import numpy as np
import tensorflow as tf

def preprocess_frame(frame):
    """Preprocess a video frame for model input."""
    frame = cv2.resize(frame, (224, 224))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = tf.keras.applications.efficientnet.preprocess_input(frame)
    return np.expand_dims(frame, axis=0)

def preprocess_image(image_path):
    """Preprocess an image for model input."""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        raise ValueError("No face detected in the image.")

    (x, y, w, h) = max(faces, key=lambda rect: rect[2] * rect[3])
    face_img = img[y:y+h, x:x+w]
    gray_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    gray_face = cv2.GaussianBlur(gray_face, (5, 5), 0)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray_face = clahe.apply(gray_face)
    gray_face = cv2.resize(gray_face, (224, 224))
    face_img = np.stack([gray_face] * 3, axis=-1)
    return tf.keras.applications.efficientnet.preprocess_input(face_img)
