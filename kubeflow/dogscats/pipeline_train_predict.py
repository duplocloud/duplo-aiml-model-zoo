import kfp
import kfp.components as comp
from typing import NamedTuple
from kfp.components import func_to_container_op, InputPath, OutputPath

dogscats_train_op = comp.load_component_from_file('component.yaml')


def dogscats_train_pipeline(datapath: str):
    # todo - pass to train.py container
    dogscats_train_op()
    return datapath #f"{datapath}/models/MobileNetVDogsCats.h5"

@func_to_container_op
def dogscats_predict_pipeline(MAPPED_PATH:str):
    from keras.models import load_model

    from keras.preprocessing import image
    from keras.utils import load_img, img_to_array
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    import numpy as np
    import os
    import pathlib

    # map to external drive
    # MAPPED_PATH = os.getenv("MAPPED_PATH", default="./data")
    data_root_path = pathlib.Path(MAPPED_PATH)
    TRAIN_DATA_DIR = f"{data_root_path}/training_set"
    VALIDATION_DATA_DIR = f"{data_root_path}/test_set"
    training_information_dir = f"{data_root_path}/training_information"
    single_prediction_dir = f"{data_root_path}/single_prediction"

    model_name = "MobileNetVDogsCats"
    models_dir = f"{data_root_path}/models"
    model_path = f"{models_dir}/{model_name}.h5"

    TRAIN_SAMPLES = 500
    VALIDATION_SAMPLES = 500
    NUM_CLASSES = 2
    IMG_WIDTH, IMG_HEIGHT = 224, 224
    BATCH_SIZE = 64

    model = load_model(model_path)

    def get_image(img_path):
        img = load_img(img_path, target_size=(IMG_WIDTH, IMG_HEIGHT))
        return img

    def predictImage(image_name):
        img = get_image(f"{single_prediction_dir}/{image_name}")
        img_array = img_to_array(img)
        expanded_img_array = img_array.reshape(-1, 224, 224, 3)
        preprocessed_img = expanded_img_array / 255.
        prediction = model.predict(preprocessed_img)
        print(prediction)
        print("{'cats': 0, 'dogs': 1}")

    predictImage("cat_or_dog_1.jpg")
    predictImage("cat_or_dog_2.jpg")


def dogsctas_train_predict_pipeline():
    output_text_path = dogscats_train_pipeline("data")
    dogscats_predict_pipeline(output_text_path) # Don't forget .output !

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(dogsctas_train_predict_pipeline, 'dogscats_train_predict_pipeline.yaml')
