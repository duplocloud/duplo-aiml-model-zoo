import darknet as dn
import os
# ./darknet detector test /opt/ml/input/data/custom_data/ts_data.data /opt/ml/input/data/yolov4/yolov4-train.cfg  /opt/ml/input/data/yolov4/yolov4-train_final.weights /opt/ml/input/data/custom_data/images/00002.jpg

# Darknet
TRAIN_DIR = os.getenv('TRAIN_DIR') #"/opt/ml/input/data/custom_data"
WEIGHT_DIR = os.getenv('WEIGHT_DIR') #"/opt/ml/input/data/yolov4"

cfg_file =  "{0]/{1}".format(WEIGHT_DIR, "yolov4-train.cfg")
weights_file =  "{0]/{1}".format(WEIGHT_DIR, "yolov4-train_final.weights")
data_file =  "{0]/{1}".format(TRAIN_DIR, "ts_data.data")

test_images_folder =  "{0]/{1}".format(TRAIN_DIR, "images")
test_image_file= "{0]/{1}".format(test_images_folder, "00002.jpg")

net = dn.load_net(cfg_file, weights_file, 0)
meta = dn.load_meta(data_file)
r = dn.detect(net, meta, test_image_file)
print(r)

# # scipy
# arr= imread('custom_data/dog.jpg')
# im = array_to_image(arr)
# r = detect2(net, meta, im)
# print(r)
#
# # OpenCV
# arr = cv2.imread('custom_data/dog.jpg')
# im = array_to_image(arr)
# dn.rgbgr_image(im)
# r = detect2(net, meta, im)
# print(r)
