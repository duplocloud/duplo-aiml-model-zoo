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
from .model_service import ModelService
# from duplo_s3_utils import DuploS3Utils
sys.path.insert(1, '/opt/ml/code/')


_service = ModelService()

def handle(data, context):
    if not _service.initialized:
        print("duplo-yolov4-infer",'Service Not Initialized, Initializing...')
        _service.initialize(context)

    if data is None:
        print("duplo-yolov4-infer",'Service Not Initialized, data is None ')
        return None

    return _service.handle(data, context)
