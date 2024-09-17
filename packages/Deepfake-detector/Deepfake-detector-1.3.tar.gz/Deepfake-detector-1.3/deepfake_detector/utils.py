import os
import gdown
import numpy as np
import tensorflow as tf
import cv2

MODEL_URL = "https://drive.google.com/uc?id=1X0RjFENxbMVT9Zvvzsu43smGq_wFiVIC"
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'deepfake_model.h5')

def download_model():
    if not os.path.exists(MODEL_PATH):
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        gdown.download(MODEL_URL, MODEL_PATH, quiet=False)
    return MODEL_PATH

def preprocess_frame(frame, frame_size=(224, 224)):
    frame = cv2.resize(frame, frame_size)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = tf.keras.applications.efficientnet.preprocess_input(frame)
    return np.expand_dims(frame, axis=0)

def set_threshold(value):
    if not (0 <= value <= 1):
        raise ValueError("Threshold must be between 0 and 1.")
    global THRESHOLD
    THRESHOLD = value
