import json
import numpy as np
import boto3

runtime = boto3.Session().client(service_name='sagemaker-runtime')

img = open('/config/workspace/docker/custom_data/images/00028.jpg', 'rb').read()
#endpoint_url = "https://runtime.sagemaker.us-west-2.amazonaws.com/endpoints/duplo-yolov4-darknet-test12-ep/invocations"
endpoint_name = "duplo-yolov4-darknet-test18-ep"
response = runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType='application/x-image',
    Body=bytearray(img)
)

# python test-endpoint.py
print("Response: \n", response)
print("Body: \n", response['Body'].read().decode('utf-8'))

