import os
import json
import subprocess
import re


TRAIN_DIR = os.getenv('TRAIN_DIR') #"/opt/ml/input/data/custom_data"
WEIGHT_DIR = os.getenv('WEIGHT_DIR') #"/opt/ml/input/yolov4"
MODEL_DIR =  "/opt/ml/model"

if __name__ == '__main__':
    data_file = "{0}/{1}".format(TRAIN_DIR, "ts_data.data")
    cfg_file = "{0}/{1}".format(WEIGHT_DIR, "yolov4-train.cfg")
    weight_file = "{0}/{1}".format(WEIGHT_DIR, "darknet53.conv.74")

    # ./darknet detector train  /app/darknet/custom_data/ts_data.data  /app/darknet/yolov4/yolov4-train.cfg /app/darknet/yolov4/darknet53.conv.74  -dont_show

    subprocess.run(["./darknet", "detector", "train", data_file, cfg_file, weight_file, "-dont_show"])

