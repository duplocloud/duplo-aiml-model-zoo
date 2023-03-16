import pathlib
import tensorflow as tf
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import imagenet_utils
import os

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

classes=['cans', 'colorless_pet', 'glass', 'nothing', 'paper', 'plastic']

def prepare_image(file):
    img = image.load_img( f"{data_root_path}/test-images/{file}", target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return tf.keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)

def get_test_batches():
    return ImageDataGenerator(preprocessing_function=tf.keras.applications.mobilenet.preprocess_input).flow_from_directory(
        directory= test_dir,
        target_size=(224, 224),
        batch_size=10,
        classes=classes
    )


def get_all_image_batches():
    return ImageDataGenerator(preprocessing_function=tf.keras.applications.mobilenet.preprocess_input).flow_from_directory(
        directory=data_dir, #test_dir,
        target_size=(224, 224),
        batch_size=10,
        classes=classes
    )

#Read model
model = load_model(model_path)


# Prediction test_batches
test_batches = get_test_batches()
predictions = model.predict(x=test_batches, verbose=0)
np.round(predictions)
print(classes,"\n", predictions)


#
# all_image_batches = get_all_image_batches()
# predictions = model.predict(x=all_image_batches, verbose=0)
# np.round(predictions) # to 1 or 0
# results = tf.keras.applications.mobilenet.decode_predictions(
#     predictions, top=5
# )
# # results = imagenet_utils.decode_predictions(predictions) # needs 20 bqtch
# print(results)
# print(classes,"\n", predictions)

preprocessed_image = prepare_image('1.jpg')
predictions_single = model.predict(preprocessed_image)
#Let's predict top 5 results
print(classes,"\n", predictions_single)