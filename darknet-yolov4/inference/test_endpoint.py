import json
import numpy as np
import boto3
import random
import time
from datetime import datetime

start_dt = datetime.now()
start_t = time.time()

runtime = boto3.Session().client(service_name='sagemaker-runtime')


def call_sm_for_img_num(img_nu):
    # img = open('/config/workspace/docker/custom_data/images/00028.jpg', 'rb').read()
    img_path = '/config/workspace/docker/custom_data/images/{0}.jpg'.format(img_nu)
    img = open(img_path, 'rb').read()

    # endpoint_name="https://runtime.sagemaker.us-west-2.amazonaws.com/endpoints/duplo-yolov4-darknet-test12-ep/invocations"
    endpoint_name = "duplo-yolov4-darknet-test19-ep"
    # endpoint_name="duplo-yolov4-darknet-test20-ep"
    response = runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType='application/x-image',
        Body=bytearray(img)
    )

    # read the prediction result and parse the json
    print("\n\n", "===================================================\n")
    print("img: \n ", img_nu, img_path)
    # print("response: \n ",response)
    # print(json.loads(response)) #.Body.read().decode('utf-8')
    print("result: \n ", response['Body'].read().decode('utf-8'))
    # Load the image bytes
    print("\n===================================================", "\n", )


def invoke_endpoint():
    try:
        nu = random.randint(1, 500)
        img_nu = format(nu, '05')
        call_sm_for_img_num(img_nu)
    except Exception as e:
        print("duplo-yolov4-infer", 'invoke_endpoint Exception!', e)


for i in range(10000):
    start_t_cur = time.time()
    invoke_endpoint()
    end_t_cur = time.time()
    print("time:", "  total:", int(end_t_cur - start_t), "  cur:", (end_t_cur - start_t_cur))

invoke_endpoint()

end_t = time.time()
print("time:", "  total:", int(end_t - start_t))

## cpu 10000
# time python test-endpoint.py
