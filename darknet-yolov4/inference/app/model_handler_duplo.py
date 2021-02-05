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
    if not _service.initialized:
        print("duplo-yolov4-infer", 'Service Not Initialized, Initializing...')
        _service.initialize(None)
    print("inference ==== content_type ", request.content_type)
    print("inference ==== content_type ", request.headers)
    content_type = request.content_type
    if content_type == "application/json": #"application/x-www-form-urlencoded":
        print("json inference ==== ", request.json)
        data = request.json
        resp = _service.handle_form_data(data, None)
        print("json inference ==== ", resp)
        return jsonify(resp)
    elif content_type == "application/octet-stream":
        # TODO; bsed on request.content_type --  json or binary image ?
        print("stream inference ==== ", len(request.data))
        data = request.data
        resp = _service.handle(data, None)
        print("stream inference ==== ", resp)
        return jsonify(resp)

if __name__ == '__main__':
    app.run()



