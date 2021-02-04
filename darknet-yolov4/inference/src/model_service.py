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

from .duplo_s3_utils import DuploS3Utils

sys.path.insert(1, '/opt/ml/code/')


class ModelService(object):
    def _list_files(self):
        pass

    def __init__(self):
        self.initialized = False
        self.model = None
        try:
            self.s3_utils = DuploS3Utils()
            self._list_files()
            self.s3_utils.download_s3_files()
            self.s3_utils.parse_class_names()
            print("duplo-yolov4-infer", 'download_s3_files' )
            # self.initialized = True
        except Exception as e:
            print("duplo-yolov4-infer", 'download_s3_files down-loading Exception!', e)


    def initialize(self, context):
        self.initialized = True
        try:
            self.model = self.s3_utils.load_model()
            print("duplo-yolov4-infer",'Model Loaded?', self.model)
            # self.initialized = True
        except Exception as e:
            print("duplo-yolov4-infer",'Model Loading Exception!',e)

    def preprocess(self, request):
        self._list_files()
        print("duplo-yolov4-infer",'REQUEST')
        dat = request[0]
        try:
            img_array = dat.get('body')
            o = io.BytesIO(img_array)
            pil_image = Image.open(o)
            input_image = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)
        except Exception as e:
            print("duplo-yolov4-infer",'Preprocessing Exception!',e)
        print("duplo-yolov4-infer",'Preprocess Completed Without Errors', type(input_image), '!')
        return  input_image

    def inference(self,model_input, conf_thresh = 0.1):
        try:
            self._list_files()
            classes, confidence, boxes = self.model.detect(model_input, confThreshold=conf_thresh, nmsThreshold=0.4, )
            print("duplo-yolov4-infer",'classes, confidence, boxes ', classes, confidence, boxes )
            return classes, confidence, boxes
        except Exception as e:
            print("duplo-yolov4-infer",'Inference Excpetion!!',e)
        return None,None,None

    def postprocess(self, inference_classes, inference_confidences, inference_out_boxes):
        self._list_files()
        return self.s3_utils.result(inference_classes,inference_confidences, inference_out_boxes)#, class_names=self.class_names)

    def handle(self, data, context):
        self._list_files()
        model_input = self.preprocess(data)
        print("duplo-yolov4-infer",'MODEL INPUT')
        out_classes, out_confidences , out_boxes =self.inference(model_input)
        print("duplo-yolov4-infer",'Model Generated output!')
        return self.postprocess(out_classes, out_confidences, out_boxes)
