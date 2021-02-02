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
sys.path.insert(1, '/opt/ml/code/')

# S3 ? #should be part of output.tar.zg
# "/opt/ml/input/data/custom_data"
#"/opt/ml/input/data/yolov4"
TRAIN_DIR = os.getenv('TRAIN_DIR')
WEIGHT_DIR = os.getenv('WEIGHT_DIR')
cfg_file =  "{0}/{1}".format(WEIGHT_DIR, "yolov4-train.cfg")
weights_file =  "{0}/{1}".format(WEIGHT_DIR, "yolov4-train_final.weights")
data_file =  "{0}/{1}".format(TRAIN_DIR, "ts_data.data")

def _list_files_g():
    try:
        print("duplo-yolov4-infer","cfg_file", cfg_file, path.exists(cfg_file))
        print("duplo-yolov4-infer","weights_file", weights_file, path.exists(weights_file))
        print("duplo-yolov4-infer","data_file", data_file, path.exists(data_file))
    except Exception as e:
        print("duplo-yolov4-infer",' Error while  _list_files_g!!', e)
    return ""

def load_model(cfg_file=cfg_file,weights_file=weights_file):
    try:
        _list_files_g()
        net = cv2.dnn_DetectionModel(cfg_file, weights_file)
        net.setInputSize(416, 416)
        net.setInputScale(1.0 / 255)
        net.setInputSwapRB(True)
    except Exception as e:
        print("duplo-yolov4-infer",'Error while loading model!!', e)
    return net

def parse_class_names():
    _list_files_g()
    labels = open(data_file).read().strip().split('\n')
    for label in labels:
        if "names" in label:
            lb_arr = label.split("=")
            class_names_file = lb_arr[1].strip()
            class_names = open(class_names_file).read().strip().split('\n')
            print("duplo-yolov4-infer","parse_class_names classes ", class_names_file, class_names)
            return class_names
    raise Exception("names = /opt/ml/input/data/custom_data/classes.names file not found", labels)

##
class_names = parse_class_names()
def result(classes, confidences, inference_out_boxes, class_names=class_names):
    try:
        res = []
        for i in range(len(classes)):
            class_id = classes[i][0]
            class_name = class_names[class_id]
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


class ModelHandler(object):
    def _list_files(self):
        files  = _list_files_g()
        print("duplo-yolov4-infer",'_list_files',files)

    def __init__(self):
        self.initialized = False
        self.model = None
        self._list_files()

    def initialize(self, context):
        self.initialized = True
        try:
            self.model = load_model()
            self.class_names = parse_class_names()
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
        return result(inference_classes,inference_confidences, inference_out_boxes)#, class_names=self.class_names)

    def handle(self, data, context):
        self._list_files()
        model_input = self.preprocess(data)
        print("duplo-yolov4-infer",'MODEL INPUT', model_input)
        out_classes, out_confidences , out_boxes =self.inference(model_input)
        print("duplo-yolov4-infer",'Model Generated output!')
        return self.postprocess(out_classes, out_confidences, out_boxes)

_service = ModelHandler()

def handle(data, context):
    if not _service.initialized:
        print("duplo-yolov4-infer",'Service Not Initialized, Initializing...')
        _service.initialize(context)

    if data is None:
        print("duplo-yolov4-infer",'Service Not Initialized, data is None ')
        return None

    return _service.handle(data, context)
