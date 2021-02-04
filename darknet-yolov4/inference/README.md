 
### darknet-yolov4/inference 

* s3 folder for train
    * images: s3://duploservices-aiops-yolo-128329325849/custom_data/
    * weights: s3://duploservices-aiops-yolo-128329325849/yolov4/
    * output: s3://duploservices-aiops-yolo-128329325849/output/
 

### ENV with defaults for sagemaker inference
* s3 folder for inference
```shell script

# ENV with defaults for sagemaker inference
S3_BUCKET="s3://duploservices-aiops-yolo-128329325849/yolov4/
WEIGHT_DIR="opt/ml/input/data/yolov4"
YOLOV4_CFG_NAME="yolov4-train.cfg"
WEIGHTS_FILE_NAME="yolov4-train_final.weights"
CLASS_NAMES_FILE="classes.names"  
```
 

aws ecr get-login 
#docker login above response (remove -e none)
pip3 install -r ../base-dockers/requirements.txt 
pip3 install -r ../inference/requirements.txt 
pip3 install -r ../train/requirements.txt 

#
export dc=11.0-cdnn8-ubuntu18.04-sm-train-v4
sudo docker build -t  duplocloud/cuda:$dc .
sudo docker pull duplocloud/cuda:$dc
sudo docker image tag duplocloud/cuda:$dc 128329325849.dkr.ecr.us-west-2.amazonaws.com/aimodels:$dc
sudo docker push  128329325849.dkr.ecr.us-west-2.amazonaws.com/aimodels:$dc
echo 128329325849.dkr.ecr.us-west-2.amazonaws.com/aimodels:$dc
echo  duplocloud/cuda:$dc
#


#
export dc=11.0-cdnn8-ubuntu18.04-sm-infer-v4
sudo docker build -t  duplocloud/cuda:$dc .
sudo docker pull duplocloud/cuda:$dc
sudo docker image tag duplocloud/cuda:$dc 128329325849.dkr.ecr.us-west-2.amazonaws.com/aimodels:$dc
sudo docker push  128329325849.dkr.ecr.us-west-2.amazonaws.com/aimodels:$dc
echo 128329325849.dkr.ecr.us-west-2.amazonaws.com/aimodels:$dc
echo  duplocloud/cuda:$dc
#

```shell script
docker  build  -t duplocloud/cuda:cpu-only-d-ubuntu20.04-v1 -f Dockerfile.duplo.cpu .; docker run  -itd -p 8080:80  duplocloud/cuda:cpu-only-d-ubuntu20.04-v1 
curl  -XPOST  --data-binary @"/Users/brighu/_duplo_code/duplo-aiml-model-zoo/tmp/darknet-yolov4/train/custom_data/images/00002.jpg" -H "Content-Type: application/octet-stream" localhost:8080/inference

```

```shell script
curl -v -XPOST http://example:port/path --data-binary @file.tar -H "Content-Type: application/octet-stream"
curl -v -POST  --data-binary @"/Users/brighu/_duplo_code/duplo-aiml-model-zoo/tmp/darknet-yolov4/train/custom_data/images/00002.jpg" -H "Content-Type: application/octet-stream" localhost:8080/inference



abc@ip-10-188-22-158:~/workspace/duplo-aiml-model-zoo/darknet-yolov4/inference$ python test-endpoint.py  
Response:
{
  'ResponseMetadata': {
    'RequestId': '928f1b93-e52c-4003-92dc-729b40c13e90',
    'HTTPStatusCode': 200,
    'HTTPHeaders': {
      'x-amzn-requestid': '928f1b93-e52c-4003-92dc-729b40c13e90',
      'x-amzn-invoked-production-variant': 'default-variant-name',
      'date': 'Tue, 02 Feb 2021 21:02:36 GMT',
      'content-type': 'application/json',
      'content-length': '55'
    },
    'RetryAttempts': 0
  },
  'ContentType': 'application/json',
  'InvokedProductionVariant': 'default-variant-name',
  'Body': <botocore.response.StreamingBodyobjectat0x7fcbd3ed2410>
}

Body:
[
  {
    "class_name": "danger",
    "confidence": 100,
    "text": "class_name = danger, confidence = 100 % "
  }
]
```