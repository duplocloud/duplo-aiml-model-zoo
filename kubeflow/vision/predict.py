import pathlib
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing import image_dataset_from_directory
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
from sklearn.metrics import confusion_matrix
from tensorflow import keras
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
from tensorflow.keras.applications import imagenet_utils
from sklearn.metrics import confusion_matrix
import itertools
import os
import shutil
import random
import matplotlib.pyplot as plt



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

def prepare_image(file):
    img = image.load_img(test_dir + file, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return tf.keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)

def get_test_batches():
    return ImageDataGenerator(preprocessing_function=tf.keras.applications.mobilenet.preprocess_input).flow_from_directory(
        directory=test_dir,
        target_size=(224, 224),
        batch_size=10,
        classes=['cans', 'colorless_pet', 'glass', 'nothing', 'paper', 'plastic']
    )


#Read model
model = load_model(model_path)


# Prediction test_batches
test_batches = get_test_batches()
predictions = model.predict(x=test_batches, verbose=0)
np.round(predictions) # to 1 or 0
cm = confusion_matrix(y_true=test_batches.classes,y_pred=np.argmax(predictions, axis=-1))
print(cm)


preprocessed_image = prepare_image('1.jpg')
predictions_single = model.predict(preprocessed_image)
print(predictions_single)