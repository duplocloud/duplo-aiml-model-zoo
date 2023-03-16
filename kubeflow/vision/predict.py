import pathlib
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing import image_dataset_from_directory
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
from sklearn.metrics import confusion_matrix


# map to external drive
MAPPED_PATH = os.getenv("MAPPED_PATH", default = "./imagedata")

# all data is within this folder ../data
data_root_path = pathlib.Path(MAPPED_PATH)
data_dir = f"{data_root_path}/images"
models_dir = f"{data_root_path}/models"
training_information_dir = f"{data_root_path}/training_information"

test_dir = f"{data_root_path}/test-images"

model_name="MobileNetV3(small)"
model_path = f"{models_dir}/{model_name}.h5"

#Read model
model = load_model(model_path)

test_batches = ImageDataGenerator(preprocessing_function=tf.keras.applications.mobilenet.preprocess_input).flow_from_directory(
    directory=test_dir,
    target_size=(224, 224),
    batch_size=10,
    classes=['cans', 'colorless_pet', 'glass', 'nothing', 'paper', 'plastic']
)

#Prediction
predictions=model.predict(x=test_batches, verbose=0)
np.round(predictions) # to 1 or 0
cm = confusion_matrix(y_true=test_batches.classes,y_pred=np.argmax(predictions, axis=-1))

print(cm)