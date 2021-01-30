FROM duplocloud/cuda:11.0-cdnn8-ubuntu18.04-v1

RUN pip3 install sagemaker-containers

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

#RUN ln -s $INPUT_PATH/data/custom_data $CODE_PATH/data/custom_data
#RUN ln -s $MODEL_PATH $CODE_PATH/output
#TODO
#TODO
#TODO

#COPY train.py $CODE_PATH
#
#ENV PYTHONPATH=$CODE_PATH
#ENV PYTHONUNBUFFERED=TRUE
#ENV PYTHONDONTWRITEBYTECODE=TRUE
#
#ENV SAGEMAKER_PROGRAM train.py
