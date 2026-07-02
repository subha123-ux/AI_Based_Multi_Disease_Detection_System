import numpy as np
from tensorflow.keras.preprocessing import image
from .ml_model import model

CLASS_NAMES = [
    "Brain Tumor",
    "Pneumonia",
    "Skin Cancer"
]

def predict_image(img_path):

    img = image.load_img(img_path, target_size=(224,224))
    img = image.img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    preds = model.predict(img)

    index = np.argmax(preds)
    confidence = float(np.max(preds))

    return CLASS_NAMES[index], confidence