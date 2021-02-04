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

# from duplo_s3_utils import DuploS3Utils
sys.path.insert(1, '/opt/ml/code/')


class DuploS3Utils:

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


    def download_s3_files(self):
        if self.HAS_S3_BUCKET:
            subprocess.Popen(["/bin/bash", "/opt/ml/code/sync_s3_yolov4.sh", self.S3_BUCKET, self.WEIGHT_DIR])
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
    def _list_files_g(self):
        try:
            print("duplo-yolov4-infer", "self.S3_BUCKET", "= ",  self.S3_BUCKET)
            print("duplo-yolov4-infer", "self.HAS_S3_BUCKET",  "= ",  self.HAS_S3_BUCKET)
            print("duplo-yolov4-infer", "self.WEIGHT_DIR",  "= ",  self.WEIGHT_DIR)
            print("duplo-yolov4-infer", "self.YOLOV4_CFG_NAME",  "= ",  self.YOLOV4_CFG_NAME)
            print("duplo-yolov4-infer", "self.WEIGHTS_FILE_NAME",  "= ",  self.WEIGHTS_FILE_NAME)
            print("duplo-yolov4-infer", "self.CLASS_NAMES_FILE",  "= ",  self.CLASS_NAMES_FILE)
            print("duplo-yolov4-infer", "self.cfg_file_path", "= ",   self.cfg_file_path)
            print("duplo-yolov4-infer", "self.weights_file_path",  "= ",  self.weights_file_path)
            print("duplo-yolov4-infer", "self.class_names_file_path",  "= ",  self.class_names_file_path)
            print("duplo-yolov4-infer", "cfg_file",  "= ",  self.cfg_file_path,  "= ",  path.exists(self.cfg_file_path))
            print("duplo-yolov4-infer", "weights_file", "= ",   self.weights_file_path, "= ",   path.exists(self.weights_file_path))
            print("duplo-yolov4-infer", "class_file",  "= ",  self.class_names_file_path,  "= ",  path.exists(self.class_names_file_path))

            print("duplo-yolov4-infer", "self.bucket_folder_name", "= ", self.bucket_folder_name)
            print("duplo-yolov4-infer", "self.bucket_name", "= ", self.bucket_name)
        except Exception as e:
            print("duplo-yolov4-infer", ' Error while  _list_files_g!!', e)
        return ""

    def load_model(self):
        try:
            self.download_s3_files()
            self.parse_class_names()
            self._list_files_g()
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





class ModelHandler(object):
    def _list_files(self):
        files  =  self.s3_utils._list_files_g()
        print("duplo-yolov4-infer",'_list_files',files)

    def __init__(self):
        self.initialized = False
        self.model = None
        try:
            self.s3_utils = DuploS3Utils()
            self._list_files()
            self.s3_utils.download_s3_files()
            self.parse_class_names()
            print("duplo-yolov4-infer", 'download_s3_files' )
            # self.initialized = True
        except Exception as e:
            print("duplo-yolov4-infer", 'download_s3_files down-loading Exception!', e)


    def initialize(self, context):
        self.initialized = True
        try:
            self.model = self.s3_utils.load_model()
            # self.class_names = self.s3_utils.parse_class_names()
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
