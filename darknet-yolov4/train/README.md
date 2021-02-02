# aiml-model-zoo

### darknet-yolov4/train 

* s3 folder
    * images: s3://duploservices-aiops-yolo-128329325849/custom_data/
    * weights: s3://duploservices-aiops-yolo-128329325849/yolov4/
    * output: s3://duploservices-aiops-yolo-128329325849/output/
* flask

### TODO


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

```
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
  "class_name = danger, confidence = 100 % boxes= "
```