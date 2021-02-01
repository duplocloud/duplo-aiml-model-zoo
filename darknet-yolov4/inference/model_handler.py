import cv2
import io
from PIL import Image
import numpy
import os
import sys
sys.path.insert(1, '/opt/ml/code/')


# ./darknet detector test /opt/ml/input/data/custom_data/ts_data.data /opt/ml/input/data/yolov4/yolov4-train.cfg  /opt/ml/input/data/yolov4/yolov4-train_final.weights /opt/ml/input/data/custom_data/images/00002.jpg

# Darknet
TRAIN_DIR = os.getenv('TRAIN_DIR') #"/opt/ml/input/data/custom_data"
WEIGHT_DIR = os.getenv('WEIGHT_DIR') #"/opt/ml/input/data/yolov4"

cfg_file =  "{0}/{1}".format(WEIGHT_DIR, "yolov4-train.cfg")
weights_file =  "{0}/{1}".format(WEIGHT_DIR, "yolov4-train_final.weights")
data_file =  "{0}/{1}".format(TRAIN_DIR, "ts_data.data")

test_images_folder =  "{0}/{1}".format(TRAIN_DIR, "images")
test_image_file= "{0}/{1}".format(test_images_folder, "00002.jpg")


def load_model(cfg_file=cfg_file,weights_file=weights_file):
    try:
        net = cv2.dnn_DetectionModel(cfg_file, weights_file)
        net.setInputSize(416, 416)
        net.setInputScale(1.0 / 255)
        net.setInputSwapRB(True)
    except Exception as e:
        print('Error while loading model!!', e)
    return net


def result(classes, confidences, class_names):
    res = []
    for i in range(len(classes)):
        class_id= classes[i][0]
        class_name = class_names[class_id]
        confidence = round(confidences[i][0] * 100)
        result_text= "class_name = {0}, confidence = {1} % ".format(class_name, confidence )
        res.append(result_text)
    print('Postprocessing Complete!', res, type(res))
    return [res]


class ModelHandler(object):
    def __init__(self):
        self.initialized = False
        self.model = None

    def initialize(self, context):
        self.initialized = True
        try:
            self.model = load_model()
            print('Model Loaded?', self.model)
        except Exception as e:
            print('Model Loading Exception!',e)
        try:
            self.model = load_model()
            print('Model Loaded?', self.model)
        except Exception as e:
            print('Model Loading Exception!',e)


    def parse_classes(self):
        labels = open(data_file).read().strip().split('\n')
        for label in labels:
            if "names" in label:
                lb_arr = label.split("=")
                classes_file = lb_arr[1].strip()
                classes = open(classes_file).read().strip().split('\n')
                print("parse_classes classes ", classes_file, classes)
                return classes
        raise Exception("names = /opt/ml/input/data/custom_data/classes.names file not found", labels)

    def preprocess(self, request):
        print('REQUEST', request)
        dat = request[0]
        try:
            img_array = dat.get('body')
            o = io.BytesIO(img_array)
            # o.seek(0)
            pil_image = Image.open(o)
            input_image = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)
        except Exception as e:
            print('Preprocessing Exception!',e)
        print('Preprocess Completed Without Errors', type(input_image), '!', input_image)
        return  input_image

    def inference(self,model_input, conf_thresh = 0.1):
        try:
            classes, confidence, boxes = self.model.detect(model_input, confThreshold=conf_thresh, nmsThreshold=0.4, )
        except Exception as e:
            print('Inference Excpetion!!',e)
        print('Classes and Confs', classes, confidence)
        return classes, confidence

    def postprocess(self, inference_classes, inference_confidences):
        return result(inference_classes,inference_confidences)

    def handle(self, data, context):

        model_input = self.preprocess(data)
        print('MODEL INPUT', model_input)
        out_classes, out_confidences =self.inference(model_input)
        print('Model Generated output!')
        return self.postprocess(out_classes, out_confidences)

_service = ModelHandler()

def handle(data, context):
    if not _service.initialized:
        print('Service Not Initialized, Initializing...')
        _service.initialize(context)

    if data is None:
        return None

    return _service.handle(data, context)



















