
import tensorflow as tf
import numpy as np
import json
import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "disease_model.keras")
CLASS_PATH = os.path.join(BASE_DIR, "..", "model", "class_indices.json")

model = tf.keras.models.load_model(MODEL_PATH)


with open(CLASS_PATH) as f:
    class_indices = json.load(f)

CLASS_NAMES = {v: k for k, v in class_indices.items()}



def predict_disease(img_path):

    img = image.load_img(img_path, target_size=(224,224))
    img = image.img_to_array(img)

    img = preprocess_input(img)

    img = np.expand_dims(img, axis=0)

    preds = model.predict(img, verbose=0)[0]

    index = np.argmax(preds)
    confidence = float(preds[index] * 100)

    disease = CLASS_NAMES[index]

    return disease, round(confidence, 2)