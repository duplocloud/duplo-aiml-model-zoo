
ARG BASE_CONTAINER=nvidia/cuda:11.2.2-cudnn8-devel-ubuntu20.04
ARG BUILDER_IMAGE=$BASE_CONTAINER
ARG BASE_IMAGE=$BASE_CONTAINER

FROM $BUILDER_IMAGE AS builder

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests -y gnupg2 ca-certificates git build-essential \
     g++ libopencv-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#    RUN apt update
#RUN apt install -y \
#    wget git vim curl zip  jq net-tools \
#    pkg-config  build-essential cmake autoconf automake \
#    clang-format  apt-utils \
#    checkinstall libtool  yasm gnupg-agent \
#    apt-transport-https  ca-certificates software-properties-common libopencv-dev \
#    g++ libopencv-dev


COPY configure.sh /tmp/
RUN chmod +x  /tmp/*.sh

ARG SOURCE_BRANCH=master
ENV SOURCE_BRANCH $SOURCE_BRANCH

ARG SOURCE_COMMIT=HEAD
ENV SOURCE_COMMIT $SOURCE_COMMIT

ARG CONFIG=default


RUN git clone https://github.com/AlexeyAB/darknet.git && cd darknet \
    && git checkout $SOURCE_BRANCH \
    && git reset --hard $SOURCE_COMMIT \
    && /tmp/configure.sh $CONFIG && make \
    && cp libdarknet.so /tmp \
    && cp darknet.py /tmp \
    && cd .. && rm -rf darknet

FROM $BASE_IMAGE

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests -y libsm6 libxext6 libxrender-dev ffmpeg \
    libopencv-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ================== python 3.8 ===========
RUN yum -y install libffi-devel
RUN yum -y install make gcc openssl-devel bzip2-devel tar
RUN wget https://www.python.org/ftp/python/3.8.7/Python-3.8.7.tgz
RUN tar xzf Python-3.8.7.tgz
WORKDIR /Python-3.8.7
RUN ./configure --enable-optimizations
RUN make altinstall
RUN ln -sfn /usr/local/bin/python3.8 /usr/bin/python3.8
RUN ln -sfn /usr/local/bin/pip3.8 /usr/bin/pip3.8
# RUN yum install -y   python3 python3-pip python3-numpy python3-matplotlib python3-scipy python3-pandas python3-simpy
#RUN update-alternatives --install "/usr/bin/python" "python" "$(which python3)" 1
RUN alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 10
RUN alternatives --install /usr/bin/python python /usr/bin/python2 20
# RUN alternatives --display python
# RUN alternatives --auto python
# RUN python3 -m pip install -U pip
RUN python3.8 -m pip install -U setuptools
#RUN yum install -y  python-pip
#RUN python -m pip install pip --upgrade

RUN python3 -m pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir numpy opencv-python
##### v
RUN pip3 install http://download.pytorch.org/whl/cu90/torch-0.4.0-cp35-cp35m-linux_x86_64.whl --upgrade && \
    pip3 install torchvision --upgrade

RUN rm -rf /var/lib/apt/lists/*
RUN rm -rf /root/.cache

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/local/lib"

# ================== python 3.8 ===========

COPY --from=builder /tmp/libdarknet.so /usr/local/darknet/libdarknet.so
COPY --from=builder /tmp/darknet.py /usr/local/darknet/darknet.py

ENV DARKNET_PATH=/usr/local/darknet
ENV PYTHONPATH "${PYTHONPATH}:/usr/local/darknet"

CMD ["python3"]


#
#
##
##ARG BASE_CONTAINER=nvidia/cuda:11.2.2-cudnn8-devel-ubuntu20.04
##ARG BUILDER_IMAGE=$BASE_CONTAINER
##ARG BASE_IMAGE=$BASE_CONTAINER
## #FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04
###FROM nvidia/cuda:11.1.1-cudnn8-devel-ubuntu20.04
###FROM nvidia/cuda:10.2-cudnn7-devel-ubuntu18.04
##
###FROM nvidia/cuda:11.0-cudnn8-devel-ubuntu18.04
##FROM $BUILDER_IMAGE
##
### docker build -t  duplocloud/cuda:11.0-cdnn8-ubuntu18.04-v2 .
### docker build -t  duplocloud/cuda:11.1.1-cdnn8-ubuntu20.04-v3 .
#
#ARG DEBIAN_FRONTEND=noninteractive
#ENV LC_ALL=C.UTF-8
#ENV LANG=C.UTF-8
#
#ENV CODE_PATH=/opt/ml/code
#ENV MODEL_PATH=/opt/ml/model
#ENV INPUT_PATH=/opt/ml/input
#
#
#RUN mkdir -p /opt/ml/code
#RUN mkdir -p /opt/ml/model/backup
#RUN mkdir -p /opt/ml/input/data/custom_data
#
#
#RUN apt update
#RUN apt install -y \
#    wget git vim curl zip  jq net-tools \
#    pkg-config  build-essential cmake autoconf automake \
#    clang-format  apt-utils \
#    checkinstall libtool  yasm gnupg-agent \
#    apt-transport-https  ca-certificates software-properties-common libopencv-dev \
#    g++ libopencv-dev
#
## ================== python 3.8 ===========
#RUN yum -y install libffi-devel
#RUN yum -y install make gcc openssl-devel bzip2-devel tar
#RUN wget https://www.python.org/ftp/python/3.8.7/Python-3.8.7.tgz
#RUN tar xzf Python-3.8.7.tgz
#WORKDIR /Python-3.8.7
#RUN ./configure --enable-optimizations
#RUN make altinstall
#RUN ln -sfn /usr/local/bin/python3.8 /usr/bin/python3.8
#RUN ln -sfn /usr/local/bin/pip3.8 /usr/bin/pip3.8
## RUN yum install -y   python3 python3-pip python3-numpy python3-matplotlib python3-scipy python3-pandas python3-simpy
##RUN update-alternatives --install "/usr/bin/python" "python" "$(which python3)" 1
#RUN alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 10
#RUN alternatives --install /usr/bin/python python /usr/bin/python2 20
## RUN alternatives --display python
## RUN alternatives --auto python
## RUN python3 -m pip install -U pip
#RUN python3.8 -m pip install -U setuptools
##RUN yum install -y  python-pip
##RUN python -m pip install pip --upgrade
#
#RUN python3 -m pip install --no-cache-dir --upgrade pip \
#    && pip install --no-cache-dir numpy opencv-python
## ================== python 3.8 ===========
#
#RUN apt-get clean autoclean
#RUN apt-get autoremove --yes
#RUN apt-get clean
#############################################
#RUN apt-get update && apt-get install -y python3  python3-pip
#RUN pip3 install scikit-build
#RUN pip3 install --upgrade cython
#RUN pip3 install --upgrade cython
#RUN pip3 install opencv-python
#RUN  python3 --version
#############################################
#############################################
## Get OpenCV dependencies
#RUN apt-get update && apt-get install -y \
#    gfortran libjpeg8-dev libtiff5-dev libavcodec-dev libavformat-dev \
#    libswscale-dev libdc1394-22-dev libxine2-dev libv4l-dev \
#    qt5-default libgtk2.0-dev libtbb-dev libatlas-base-dev \
#    libfaac-dev libmp3lame-dev libtheora-dev libvorbis-dev libxvidcore-dev libopencore-amrnb-dev \
#    libopencore-amrwb-dev x264 v4l-utils libprotobuf-dev protobuf-compiler libgoogle-glog-dev \
#    libgflags-dev libgphoto2-dev
#RUN apt-get clean autoclean
#RUN apt-get autoremove --yes
#RUN apt-get clean
#############################################
## build darknet
#WORKDIR /opt/ml/code
#RUN git clone https://github.com/AlexeyAB/darknet.git ./
##RUN make OPENCV=1 GPU=1 AVX=1 OPENMP=1 CUDNN=1 CUDNN_HALF=0 OPENMP=1 -j $(nproc)
##RUN make   GPU=1   CUDNN=1 OPENCV=1
#RUN make OPENCV=1 GPU=1 AVX=1 OPENMP=1 CUDNN=1 CUDNN_HALF=0 OPENMP=1 LIBSO=1
#RUN chmod +x darknet
#############################################
#
#######
## build opencv
#RUN cd /opt && git clone --verbose https://github.com/opencv/opencv.git -b 4.4.0 &&\
#    cd /opt && wget https://github.com/opencv/opencv_contrib/archive/4.4.0.tar.gz &&\
#    mkdir opencv_contrib && tar -xf 4.4.0.tar.gz -C opencv_contrib --strip-components 1
#RUN cd /opt/opencv && mkdir release && cd release && \
#         cmake -G "Unix Makefiles" \
#        -DENABLE_PRECOMPILED_HEADERS=OFF \
#        -DCMAKE_CXX_COMPILER=/usr/bin/g++ \
#        -DCMAKE_C_COMPILER=/usr/bin/gcc \
#        -DCMAKE_BUILD_TYPE=RELEASE \
#        -DCMAKE_INSTALL_PREFIX=/usr/local \
#        -DWITH_TBB=ON \
#        -DBUILD_NEW_PYTHON_SUPPORT=ON \
#        -DWITH_V4L=ON \
#        -DINSTALL_C_EXAMPLES=OFF \
#        -DINSTALL_PYTHON_EXAMPLES=ON \
#        -DBUILD_EXAMPLES=OFF \
#        -DWITH_QT=ON \
#        -DWITH_OPENGL=ON \
#        -DWITH_CUDA=ON \
#        -DWITH_CUDNN=ON \
#        -DCUDA_ARCH_BIN=70 \
#        -DOPENCV_DNN_CUDA=ON \
#        -DCUDA_GENERATION=Auto \
#        -DOPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
#        .. &&\
#        make -j"$(nproc)"  && \
#        make install && \
#        ldconfig &&\
#        cd /opt/opencv/release && make clean
#
########### moved to base #####
#RUN pip3 install sagemaker-containers
###########
#ENV RUSTUP_HOME=/usr/local/rustup
#ENV CARGO_HOME=/usr/local/cargo
#ENV PATH=/usr/local/cargo/bin:$PATH:$HOME/.cargo/bin
#RUN set -eux; \
#    url="https://static.rust-lang.org/rustup/dist/x86_64-unknown-linux-gnu/rustup-init"; \
#    wget "$url"; \
#    chmod +x rustup-init; \
#    ./rustup-init -y --no-modify-path --default-toolchain nightly; \
#    rm rustup-init; \
#    chmod -R a+w $RUSTUP_HOME $CARGO_HOME;
#RUN  rustup --version;
#RUN  cargo --version;
#RUN  rustc --version;
#
#RUN apt update -y; apt-get install -y clang
#RUN pip3 install darknetpy
########### moved to base #####
#
############################################
#RUN pip3 list
#COPY ./requirements.txt .
#RUN  python3 --version
#RUN pip3 install -r requirements.txt
############################################
#
#
#######
## check : reduce docker size ?
##RUN df -h
##RUN du -h -d 1 /opt
#######
#RUN apt-get clean autoclean
#RUN apt-get autoremove --yes
#RUN rm -rf /var/lib/{apt,dpkg,cache,log}/
#RUN rm -rf /var/lib/apt/lists/*
#RUN touch /tmp/aa
#
#################
#RUN pip3 list
############################################
#RUN ls /opt/ml/code/
#WORKDIR /opt/ml/code
#ENV LIBRARY_PATH ./:/usr/local/lib:$LIBRARY_PATH
##keep the relevent one below
#ENV LD_LIBRARY_PATH=/usr/local/cuda-10.1/lib64:/usr/local/cuda-10.1/bin:/usr/local/cuda-10.1/targets/x86_64-linux/lib/:/usr/local/cuda-10.1/compat/:$LD_LIBRARY_PATH
#ENV LD_LIBRARY_PATH=/usr/local/cuda-11.1.1/lib64:/usr/local/cuda-11.1.1/bin:/usr/local/cuda-11.1.1/targets/x86_64-linux/lib/:/usr/local/cuda-11.1.1/compat/:$LD_LIBRARY_PATH
#ENV LD_LIBRARY_PATH=/usr/local/cuda-11.1/lib64:/usr/local/cuda-11.1/bin:/usr/local/cuda-11.1/targets/x86_64-linux/lib/:/usr/local/cuda-11.1/compat/:$LD_LIBRARY_PATH
#ENV LD_LIBRARY_PATH=/usr/local/cuda-11.0/lib64:/usr/local/cuda-11.0/bin:/usr/local/cuda-11.0/targets/x86_64-linux/lib/:/usr/local/cuda-11.0/compat/:$LD_LIBRARY_PATH
#ENV LD_LIBRARY_PATH=/usr/local/cuda-11.2/lib64:/usr/local/cuda-10.2/bin:/usr/local/cuda-10.2/targets/x86_64-linux/lib/:/usr/local/cuda-10.2/compat/:$LD_LIBRARY_PATH
#ENV PATH=$PATH:/opt/VirtualGL/bin
#
#
#
