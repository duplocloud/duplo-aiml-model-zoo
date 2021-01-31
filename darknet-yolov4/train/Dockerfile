#FROM duplocloud/cuda:11.1.1-cdnn8-ubuntu20.04-v1
FROM duplocloud/cuda:11.0-cdnn8-ubuntu18.04-v1
#11.1.1-cdnn8-ubuntu20.04-v1

########## move to base #####
RUN pip3 install sagemaker-containers
##########
ENV LD_LIBRARY_PATH=/usr/local/lib:/usr/local/cuda-11.0/targets/x86_64-linux/lib/:/usr/local/cuda-11.0/compat/:$LD_LIBRARY_PATH
ENV PATH=$LD_LIBRARY_PATH:$PATH

ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH
RUN set -eux; \
    \
    url="https://static.rust-lang.org/rustup/dist/x86_64-unknown-linux-gnu/rustup-init"; \
    wget "$url"; \
    chmod +x rustup-init; \
    ./rustup-init -y --no-modify-path --default-toolchain nightly; \
    rm rustup-init; \
    chmod -R a+w $RUSTUP_HOME $CARGO_HOME; \
    rustup --version; \
    cargo --version; \
    rustc --version;

RUN apt update -y; apt-get install -y clang
RUN pip3 install darknetpy
########## move to base #####

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

#RUN ln -s $INPUT_PATH/data/custom_data $CODE_PATH/data/custom_data
#RUN ln -s $MODEL_PATH $CODE_PATH/output
COPY *custom_data /opt/ml/input/data/custom_data/
COPY *yolov4 /opt/ml/input/data/yolov4/
COPY *.py $CODE_PATH/
COPY train.py $CODE_PATH

ENV PYTHONPATH=$CODE_PATH
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE


##########
# ./darknet detector test /opt/ml/input/data/custom_data/ts_data.data /opt/ml/input/data/yolov4/yolov4-train.cfg  /opt/ml/input/data/yolov4/yolov4-train_final.weights /opt/ml/input/data/custom_data/images/00002.jpg


ENV SAGEMAKER_PROGRAM train.py
