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
from .model_service_duplo import ModelService

from flask import Flask, jsonify, request
import base64
from flask import Flask
app = Flask(__name__)


print("duplo-yolov4-infer",'ModelService, Initializing...')
_service = ModelService()
print("duplo-yolov4-infer",'ModelService Initialized,')

@app.route("/")
def duplo_aiml():
    return "Hello, duplo_aiml-world!"

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'data': 'pong!'})

@app.route('/inference', methods=['POST'])
def inference( ):
    print("inference ==== content_type ", request.content_type)
    print("inference ==== content_type ", request.headers)
    # TODO; bsed on request.content_type --  json or binary image ?
    # print("inference ==== ", request.data)
    data = request.data
    if not _service.initialized:
        print("duplo-yolov4-infer", 'Service Not Initialized, Initializing...')
        _service.initialize(None)
    resp = _service.handle(data, None)
    print("inference ==== ", resp)
    return jsonify(resp)

if __name__ == '__main__':
    app.run()



