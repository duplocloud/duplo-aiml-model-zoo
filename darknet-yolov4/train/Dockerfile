#FROM duplocloud/cuda:11.1.1-cdnn8-ubuntu20.04-v1
#FROM duplocloud/cuda:11.0-cdnn8-ubuntu18.04-v1
#FROM duplocloud/cuda:11.0-cdnn8-ubuntu18.04-v2
#FROM duplocloud/cuda:11.1.1-cdnn8-ubuntu20.04-v2
#FROM duplocloud/cuda:11.1.1-cdnn8-ubuntu20.04-v3

FROM duplocloud/cuda:11.0-cdnn8-ubuntu18.04-v3


#
#export dc=11.0-cdnn8-ubuntu18.04-sm-train-v4
#sudo docker build -t  duplocloud/cuda:$dc .
#sudo docker pull duplocloud/cuda:$dc
#sudo docker image tag duplocloud/cuda:$dc 128329325849.dkr.ecr.us-west-2.amazonaws.com/aimodels:$dc
#sudo docker push  128329325849.dkr.ecr.us-west-2.amazonaws.com/aimodels:$dc
#echo 128329325849.dkr.ecr.us-west-2.amazonaws.com/aimodels:$dc
#echo  duplocloud/cuda:$dc
# #./darknet detector test /opt/ml/input/data/custom_data/ts_data.data /opt/ml/input/data/yolov4/yolov4-train.cfg  /opt/ml/input/data/yolov4/yolov4-train_final.weights /opt/ml/input/data/custom_data/images/00002.jpg
#


############
COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

# code and data files
ENV CODE_PATH=/opt/ml/code
ENV MODEL_PATH=/opt/ml/model
ENV INPUT_PATH=/opt/ml/input/data

ARG TRAIN_CHANNEL=custom_data
ARG WEIGHT_CHANNEL=yolov4

ENV TRAIN_DIR $INPUT_PATH/$TRAIN_CHANNEL
ENV WEIGHT_DIR $INPUT_PATH/$WEIGHT_CHANNEL

RUN echo $TRAIN_DIR
RUN echo $WEIGHT_DIR

RUN mkdir -p /opt/ml/code
RUN mkdir -p /opt/ml/model
RUN mkdir -p /opt/ml/input/data/custom_data
RUN mkdir -p /opt/ml/input/data/yolov4

COPY *custom_data /opt/ml/input/data/custom_data/
COPY *yolov4 /opt/ml/input/data/yolov4/
COPY *.py $CODE_PATH/
COPY train.py $CODE_PATH

ENV PYTHONPATH=$CODE_PATH
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE

##############
#RUN cp /tmp/darknet-master/libdarknet.so /usr/local/lib/libdarknet.so
#keep the relevent one below
ENV LIBRARY_PATH ./:/usr/local/lib:$LIBRARY_PATH
ENV LD_LIBRARY_PATH=/usr/local/cuda-10.1/targets/x86_64-linux/lib/:/usr/local/cuda-10.1/compat/:$LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH=/usr/local/cuda-11.1.1/targets/x86_64-linux/lib/:/usr/local/cuda-11.1.1/compat/:$LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH=/usr/local/cuda-11.0/targets/x86_64-linux/lib/:/usr/local/cuda-11.0/compat/:$LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH=/usr/local/cuda-10.2/targets/x86_64-linux/lib/:/usr/local/cuda-10.2/compat/:$LD_LIBRARY_PATH

# env for  SAGEMAKER_PROGRAM
ENV SAGEMAKER_PROGRAM train.py
