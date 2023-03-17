import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import  keras
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from keras.layers import Input, Flatten, Dense, Dropout, GlobalAveragePooling2D
from keras.applications.mobilenet import MobileNet
import math
import pathlib
import os

# map to external drive
MAPPED_PATH = os.getenv("MAPPED_PATH", default = "./data")
data_root_path = pathlib.Path(MAPPED_PATH)
TRAIN_DATA_DIR = f"{data_root_path}/training_set"
VALIDATION_DATA_DIR =  f"{data_root_path}/test_set"
training_information_dir = f"{data_root_path}/training_information"
single_prediction_dir = f"{data_root_path}/single_prediction"


model_name="MobileNetVDogsCats"
models_dir = f"{data_root_path}/models"
model_path = f"{models_dir}/{model_name}.h5"

TRAIN_SAMPLES = 500
VALIDATION_SAMPLES = 500
NUM_CLASSES=2
IMG_WIDTH, IMG_HEIGHT = 224, 224
BATCH_SIZE=64

train_datagen = ImageDataGenerator(rescale=1./255,
                                   rotation_range=20,
                                   width_shift_range=0.2,
                                   height_shift_range=0.2,
                                   zoom_range=0.2)

val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
                        TRAIN_DATA_DIR,
                        target_size=(IMG_WIDTH, IMG_HEIGHT),
                        batch_size=BATCH_SIZE,
                        shuffle=True,
                        seed=12345,
                        class_mode='categorical')

validation_generator = val_datagen.flow_from_directory(
                        VALIDATION_DATA_DIR,
                        target_size=(IMG_WIDTH, IMG_HEIGHT),
                        batch_size=BATCH_SIZE,
                        shuffle=False,
                        class_mode='categorical')


def model_maker():
    base_model = tf.keras.applications.MobileNet(include_top=False, input_shape=(IMG_WIDTH, IMG_HEIGHT, 3))

    for layer in base_model.layers[:]:
        layer.trainable = False  # Freeze the layers

    input = tf.keras.Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3))
    custom_model = base_model(input)
    custom_model = tf.keras.layers.GlobalAveragePooling2D()(custom_model)
    custom_model = tf.keras.layers.Dense(64, activation='relu')(custom_model)
    custom_model = tf.keras.layers.Dropout(0.5)(custom_model)
    predictions = tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')(custom_model)

    return tf.keras.Model(inputs=input, outputs=predictions)

model = model_maker()

model.compile(loss='categorical_crossentropy',
              optimizer= keras.optimizers.Adam(lr=0.001),
              metrics=['acc'])

model.fit_generator(train_generator,
                    steps_per_epoch = math.ceil(float(TRAIN_SAMPLES) / BATCH_SIZE),
                    epochs=10,
                    validation_data = validation_generator,
                    validation_steps = math.ceil(float(VALIDATION_SAMPLES) / BATCH_SIZE))
model.save(model_path)