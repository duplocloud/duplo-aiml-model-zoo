import sys, os
import boto3
import subprocess
import cv2
import io
from PIL import Image
import numpy
import os
import sys
import subprocess
import glob
import os.path
from os import path
import boto3
import json
from subprocess import Popen


class DuploS3Utils:

    # ENV with defaults for sagemaker inference
    # S3_BUCKET="s3://duploservices-aiops-yolo-128329325849/yolov4/
    # WEIGHT_DIR=opt/ml/input/data/yolov4
    # YOLOV4_CFG_NAME=yolov4-train.cfg
    # WEIGHTS_FILE_NAME=yolov4-train_final.weights
    # CLASS_NAMES_FILE=classes.names

    def __init__(self):
        self.S3_BUCKET = os.getenv('S3_BUCKET', "s3://duploservices-aiops-yolo-128329325849/yolov4/")
        self.HAS_S3_BUCKET = os.getenv('S3_BUCKET') is not None

        self.WEIGHT_DIR = os.getenv('WEIGHT_DIR', "/opt/ml/input/data/yolov4")
        self.YOLOV4_CFG_NAME = os.getenv('YOLOV4_CFG_NAME', "yolov4-train.cfg")
        self.WEIGHTS_FILE_NAME = os.getenv('WEIGHTS_FILE_NAME', "yolov4-train_final.weights")
        self.CLASS_NAMES_FILE = os.getenv('CLASS_NAMES_FILE', "classes.names")

        self.cfg_file_path = "{0}/{1}".format(self.WEIGHT_DIR, self.YOLOV4_CFG_NAME)
        self.weights_file_path  = "{0}/{1}".format(self.WEIGHT_DIR, self.WEIGHTS_FILE_NAME)
        self.class_names_file_path  = "{0}/{1}".format(self.WEIGHT_DIR, self.CLASS_NAMES_FILE)

        self.download_s3_files()
        self._list_files_g()

    def _list_files_g(self):
        val = {}
        try:
            val["S3_BUCKET"] = self.S3_BUCKET
            val["HAS_S3_BUCKET"] = self.HAS_S3_BUCKET

            val["WEIGHT_DIR"] = self.WEIGHT_DIR

            val["YOLOV4_CFG_NAME"] = self.YOLOV4_CFG_NAME
            val["WEIGHTS_FILE_NAME"] = self.WEIGHTS_FILE_NAME
            val["CLASS_NAMES_FILE"] = self.CLASS_NAMES_FILE

            val["weights_file_path"] = self.weights_file_path
            val["class_names_file_path"] = self.class_names_file_path
            val["cfg_file_path"] = self.cfg_file_path

            val["cfg_file_path_EXISTS"] = path.exists(self.cfg_file_path)
            val["weights_file_path_EXISTS"] = path.exists(self.weights_file_path)
            val["class_names_file_path_EXISTS"] = path.exists(self.class_names_file_path)

            val["bucket_folder_name"] = self.bucket_folder_name
            val["bucket_name"] = self.bucket_name
        except Exception as e:
            print("duplo-yolov4-infer", ' Error while  _list_files_g!!', e)
        print(json.dumps(val, indent=2))
        return ""

    def download_s3_files(self):
        if self.HAS_S3_BUCKET:
            # process = Popen(['/opt/ml/code/sync_s3_yolov4.sh', str(self.S3_BUCKET), str(self.WEIGHT_DIR)], shell=True)
            # subprocess.Popen(["/bin/bash", "/opt/ml/code/sync_s3_yolov4.sh", self.S3_BUCKET, self.WEIGHT_DIR])
            # result_cmd = subprocess.check_output(['/opt/ml/code/sync_s3_yolov4.sh', str(self.S3_BUCKET), str(self.WEIGHT_DIR)])
            # print(result_cmd)
            os.system("/opt/ml/code/sync_s3_yolov4.sh {} {}".format(str(self.S3_BUCKET), str(self.WEIGHT_DIR)))
            ## alternate way
            file_done = os.path.join(self.WEIGHT_DIR, "download_complete")
            if not os.path.exists(file_done):
                try:
                    s3 = boto3.resource('s3')
                    # "s3://duploservices-aiops-yolo-128329325849/yolov4/"
                    bucket_path = self.S3_BUCKET.replace("s3://","").strip()
                    bucket_arr = bucket_path.split("/")
                    bucket_name = bucket_arr[0]
                    bucket_folder_name = ""
                    if len(bucket_name) > 0:
                        bucket_arr2 = bucket_arr[1 :]
                        bucket_folder_name = "/".join(bucket_arr2).strip()

                    self.bucket_folder_name = bucket_folder_name
                    self.bucket_name = bucket_name
                    print("duplo-yolov4-infer", "self.bucket_folder_name", "= ", self.bucket_folder_name)
                    print("duplo-yolov4-infer", "self.bucket_name", "= ", self.bucket_name)
                    s3_bucket = s3.Bucket(bucket_name)

                    # download file into current directory
                    if self.bucket_folder_name == "":
                        for s3_object in s3_bucket.objects.all():
                            local_path = os.path.join(self.WEIGHT_DIR, filename)
                            print("duplo-yolov4-infer", "download? s3 local_path", "= ", local_path)
                            if s3_object.key != self.WEIGHT_DIR:
                                path, filename = os.path.split(s3_object.key)
                                s3_bucket.download_file(s3_object.key, local_path)
                    else:
                        for s3_object in s3_bucket.objects.filter(Prefix = bucket_folder_name):
                            local_path = os.path.join(self.WEIGHT_DIR, filename)
                            print("duplo-yolov4-infer", "download? s3 local_path", "= ", local_path)
                            if s3_object.key != self.WEIGHT_DIR:
                                path, filename = os.path.split(s3_object.key)
                                local_path = os.path.join(self.WEIGHT_DIR, filename)
                                print("duplo-yolov4-infer", "downlaoding s3 local_path", "= ", local_path)
                                s3_bucket.download_file(s3_object.key, local_path)
                    #avoid multiple downloads
                    filewrite = open("file_done", "w")
                    filewrite.write("done")
                    filewrite.close()
                except Exception as e:
                    print("duplo-yolov4-infer",'Error while loading model!!', e)


    def load_model(self):
        try:
            self.download_s3_files()
            self.parse_class_names()
            net = cv2.dnn_DetectionModel( self.cfg_file_path, self.weights_file_path)
            net.setInputSize(416, 416)
            net.setInputScale(1.0 / 255)
            net.setInputSwapRB(True)
        except Exception as e:
            print("duplo-yolov4-infer", 'Error while loading model!!', e)
        return net

    def parse_class_names(self):
        self.class_names = open(self.class_names_file_path).read().strip().split('\n')
        return self.class_names
        # raise Exception("names = /opt/ml/input/data/custom_data/classes.names file not found", class_names)

    def result(self, classes, confidences, inference_out_boxes):
        try:
            res = []
            for i in range(len(classes)):
                class_id = classes[i][0]
                class_name = self.class_names[class_id]
                confidence = round(confidences[i][0] * 100)
                # boxes =  inference_out_boxes[i]
                result_text = "class_name = {0}, confidence = {1} % ".format(class_name, confidence)
                result_dict={}
                result_dict["class_name"]=class_name
                result_dict["confidence"] = confidence
                result_dict["text"] = result_text
                print("duplo-yolov4-infer","result_text", i, result_text)
                res.append(result_dict)
            print("duplo-yolov4-infer",'Postprocessing Complete!', res, type(res))
            return [res]
        except Exception as e:
            print("duplo-yolov4-infer",'Error while loading model!!', e)
        return ["error in inference"]


