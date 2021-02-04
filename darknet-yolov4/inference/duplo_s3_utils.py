import sys, os
import boto3
import subprocess


class DuploS3Utils:

    def __init__(self):
        self.S3_BUCKET = os.getenv('S3_BUCKET', "s3://duploservices-aiops-yolo-128329325849/yolov4/")
        self.HAS_S3_BUCKET = os.getenv('S3_BUCKET') is not None

        self.WEIGHT_DIR = os.getenv('TRAIN_DIR', "/opt/ml/input/data/yolov4")
        self.YOLOV4_CFG_NAME = os.getenv('TRAIN_DIR', "yolov4-train.cfg")
        self.WEIGHTS_FILE_NAME = os.getenv('TRAIN_DIR', "yolov4-train_final.weights")
        self.CLASS_NAMES_FILE = os.getenv('TRAIN_DIR', "classes.names")

        self.cfg_file_path = "{0}/{1}".format(self.WEIGHT_DIR, self.YOLOV4_CFG_NAME)
        self.weights_file_path  = "{0}/{1}".format(self.WEIGHT_DIR, self.WEIGHTS_FILE_NAME)
        self.class_names_file_path  = "{0}/{1}".format(self.WEIGHT_DIR, self.WEIGHT_DIR)

    def download_s3_files(self):
        if self.HAS_S3_BUCKET:
            subprocess.Popen(["/bin/bash", "/opt/ml/code/sync_s3_yolov4.sh", self.S3_BUCKET, self.class_names_file_path])


