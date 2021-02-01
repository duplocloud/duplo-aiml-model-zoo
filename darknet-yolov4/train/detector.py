import numpy as np
import argparse
import cv2
import os
import time
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


def extract_boxes_confidences_classids(outputs, confidence, width, height, labels, class_labels):
    boxes = []
    confidences = []
    classIDs = []

    for output in outputs:
        for detection in output:
            # Extract the scores, classid, and the confidence of the prediction
            scores = detection[5:]
            classID = np.argmax(scores)
            conf = scores[classID]

            # Consider only the predictions that are above the confidence threshold
            if conf > confidence:
                print("labels ===== ", classID, class_labels[classID])
                # Scale the bounding box back to the size of the image
                box = detection[0:4] * np.array([width, height, width, height])
                centerX, centerY, w, h = box.astype('int')

                # Use the center coordinates, width and height to get the coordinates of the top left corner
                x = int(centerX - (w / 2))
                y = int(centerY - (h / 2))

                boxes.append([x, y, int(w), int(h)])
                confidences.append(float(conf))
                classIDs.append(classID)
    print("boxes, confidences, classIDs", boxes, confidences, classIDs)
    return boxes, confidences, classIDs


def draw_bounding_boxes(image, boxes, confidences, classIDs, idxs, colors, class_labels):
    if len(idxs) > 0:
        for i in idxs.flatten():
            # extract bounding box coordinates
            x, y = boxes[i][0], boxes[i][1]
            w, h = boxes[i][2], boxes[i][3]

            # draw the bounding box and label on the image
            color = [int(c) for c in colors[classIDs[i]]]
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.4f}: {}".format(labels[classIDs[i]], confidences[i], class_labels[classIDs[i]])
            cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            print("text", text)

    return image


def make_prediction(net, layer_names, labels, image, confidence, threshold, class_labels):
    height, width = image.shape[:2]

    # Create a blob and pass it through the model
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(layer_names)

    # Extract bounding boxes, confidences and classIDs
    boxes, confidences, classIDs = extract_boxes_confidences_classids(outputs, confidence, width, height,labels, class_labels)

    # Apply Non-Max Suppression
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence, threshold)

    return boxes, confidences, classIDs, idxs


def parse_classes(labels):
    for label in labels:
        print("parse_classes" , label )
        if "names" in label:
            lb_arr = label.split("=")
            classes_file = lb_arr[1].strip()
            print("parse_classes names ", classes_file, label)
            classes = open(classes_file).read().strip().split('\n')
            print("parse_classes classes ", classes_file, classes)
            return classes
    return []
if __name__ == '__main__':
    parser = argparse.ArgumentParser()


    parser.add_argument('-w', '--weights', type=str, default=weights_file, help='Path to model weights')
    parser.add_argument('-cfg', '--config', type=str, default=cfg_file, help='Path to configuration file')
    parser.add_argument('-l', '--labels', type=str, default=data_file, help='Path to label file')
    parser.add_argument('-c', '--confidence', type=float, default=0.5,
                        help='Minimum confidence for a box to be detected.')
    parser.add_argument('-t', '--threshold', type=float, default=0.3, help='Threshold for Non-Max Suppression')
    parser.add_argument('-u', '--use_gpu', default=True, action='store_true',
                        help='Use GPU (OpenCV must be compiled for GPU). For more info checkout: https://www.pyimagesearch.com/2020/02/03/how-to-use-opencvs-dnn-module-with-nvidia-gpus-cuda-and-cudnn/')
    parser.add_argument('-s', '--save', default=False, action='store_true',
                        help='Whether or not the output should be saved')
    parser.add_argument('-sh', '--show', default=False, action="store_false", help='Show output')
    parser.add_argument('-i', '--image_path', type=str, default='/opt/ml/input/data/custom_data/images/00002.jpg', help='Path to the image file.')

    args = parser.parse_args()

    # Get the labels
    labels = open(args.labels).read().strip().split('\n')
    print("labels","len(labels)" , len(labels), labels)
    class_labels = parse_classes(labels)
    parse_classes(labels)
    # Create a list of colors for the labels
    colors = np.random.randint(0, 255, size=(len(labels), 3), dtype='uint8')

    # Load weights using OpenCV
    net = cv2.dnn.readNetFromDarknet(args.config, args.weights)

    if args.use_gpu:
        print('Using GPU')
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    if args.save:
        print('Creating output directory if it doesn\'t already exist')
        os.makedirs('output', exist_ok=True)

    # Get the ouput layer names
    layer_names = net.getLayerNames()
    layer_names = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    image = cv2.imread(args.image_path)

    boxes, confidences, classIDs, idxs = make_prediction(net, layer_names, labels, image, args.confidence,
                                                         args.threshold, class_labels)
    print("boxes", boxes)
    print("confidences", confidences)
    print("classIDs", classIDs)
    print("idxs", idxs)

    image = draw_bounding_boxes(image, boxes, confidences, classIDs, idxs, colors, class_labels)

    # show the output image
    if args.show:
        cv2.imshow('YOLO Object Detection', image)
        cv2.waitKey(0)

    if args.save:
        cv2.imwrite(f'output/{args.image_path.split("/")[-1]}', image)
    cv2.destroyAllWindows()

