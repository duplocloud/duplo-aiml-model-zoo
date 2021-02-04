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
sys.path.insert(1, '/opt/ml/code/')
sys.path.insert(1, '.')
# from flask_cors import CORS
import os
# configuration
DEBUG = True
from .model_service import ModelService

from flask import Flask, jsonify, request
import base64
from flask import Flask
app = Flask(__name__)


print("duplo-yolov4-infer",'ModelService, Initializing...')
_service = ModelService()
print("duplo-yolov4-infer",'ModelService Initialized,')

def handle(data, context):
    if not _service.initialized:
        print("duplo-yolov4-infer",'Service Not Initialized, Initializing...')
        _service.initialize(context)

    if data is None:
        print("duplo-yolov4-infer",'Service Not Initialized, data is None ')
        return None

    return _service.handle(data, context)


@app.route("/")
def duplo_aiml():
    return "Hello, duplo_aiml-world!"



@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'data': 'pong!'})

@app.route('/inference', methods=['POST'])
def inference( ):
   print("inference ==== ", request.data)
   data =  request.data
   resp = _service.handle(data, None)
   print("inference ==== ", resp)
   return resp

if __name__ == '__main__':
    app.run()



