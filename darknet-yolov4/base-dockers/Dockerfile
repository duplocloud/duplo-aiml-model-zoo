#FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04
FROM nvidia/cuda:11.0-cudnn8-devel-ubuntu18.04
#FROM nvidia/cuda:10.2-cudnn7-devel-ubuntu18.04


ARG DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV LIBRARY_PATH $LIBRARY_PATH:/usr/local/cuda/lib64/stubs

ENV CODE_PATH=/opt/ml/code
ENV MODEL_PATH=/opt/ml/model
ENV INPUT_PATH=/opt/ml/input


RUN mkdir -p /opt/ml/code
RUN mkdir -p /opt/ml/model/backup
RUN mkdir -p /opt/ml/input/data/custom_data


RUN apt update
RUN apt install -y \
    wget git vim curl zip  jq net-tools \
    pkg-config  build-essential cmake autoconf automake \
    clang-format  apt-utils \
    checkinstall libtool  yasm gnupg-agent \
    apt-transport-https  ca-certificates software-properties-common libopencv-dev

RUN apt-get clean autoclean
RUN apt-get autoremove --yes
RUN apt-get clean
############################################
RUN apt-get update && apt-get install -y python3  python3-pip
RUN pip3 install scikit-build
RUN pip3 install --upgrade cython
RUN pip3 install opencv-python
RUN  python3 --version
############################################
############################################
# Get OpenCV dependencies
RUN apt-get update && apt-get install -y \
    gfortran libjpeg8-dev libtiff5-dev libavcodec-dev libavformat-dev \
    libswscale-dev libdc1394-22-dev libxine2-dev libv4l-dev \
    qt5-default libgtk2.0-dev libtbb-dev libatlas-base-dev \
    libfaac-dev libmp3lame-dev libtheora-dev libvorbis-dev libxvidcore-dev libopencore-amrnb-dev \
    libopencore-amrwb-dev x264 v4l-utils libprotobuf-dev protobuf-compiler libgoogle-glog-dev \
    libgflags-dev libgphoto2-dev
RUN apt-get clean autoclean
RUN apt-get autoremove --yes
RUN apt-get clean
############################################
# build darknet
WORKDIR /opt/ml/code
RUN git clone https://github.com/AlexeyAB/darknet.git ./
#RUN make OPENCV=1 GPU=1 AVX=1 OPENMP=1 CUDNN=1 CUDNN_HALF=0 OPENMP=1 -j $(nproc)
RUN make   GPU=1   CUDNN=1 OPENCV=1
############################################

######
# build opencv
RUN cd /opt && git clone --verbose https://github.com/opencv/opencv.git -b 4.4.0 &&\
    cd /opt && wget https://github.com/opencv/opencv_contrib/archive/4.4.0.tar.gz &&\
    mkdir opencv_contrib && tar -xf 4.4.0.tar.gz -C opencv_contrib --strip-components 1
RUN cd /opt/opencv && mkdir release && cd release && \
    cmake -G "Unix Makefiles" -DENABLE_PRECOMPILED_HEADERS=OFF -DCMAKE_CXX_COMPILER=/usr/bin/g++ \
    CMAKE_C_COMPILER=/usr/bin/gcc -DCMAKE_BUILD_TYPE=RELEASE -DCMAKE_INSTALL_PREFIX=/usr/local \
    -DWITH_TBB=ON -DBUILD_NEW_PYTHON_SUPPORT=ON -DWITH_V4L=ON -DINSTALL_C_EXAMPLES=OFF \
    -DINSTALL_PYTHON_EXAMPLES=ON -DBUILD_EXAMPLES=OFF -DWITH_QT=ON -DWITH_OPENGL=ON \
    -DWITH_CUDA=ON -DWITH_CUDNN=ON -DCUDA_ARCH_BIN=70 -DOPENCV_DNN_CUDA=ON -DCUDA_GENERATION=Auto -DOPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
    .. &&\
    make -j"$(nproc)"  && \
    make install && \
    ldconfig &&\
    cd /opt/opencv/release && make clean

###########################################
RUN pip3 list
COPY ./requirements.txt .
RUN  python3 --version
RUN pip3 install -r requirements.txt
###########################################
######
# check : reduce docker size ?
#RUN df -h
#RUN du -h -d 1 /opt
######
RUN apt-get clean autoclean
RUN apt-get autoremove --yes
RUN rm -rf /var/lib/{apt,dpkg,cache,log}/
RUN rm -rf /var/lib/apt/lists/*
RUN touch /tmp/aa
RUN rm /tmp/*
#RUN pip cache purge
###########################################
#######
# check : reduce docker size ?
#RUN du -h -d 1 /opt
#RUN du -h -d 1 ~/.
#######

RUN chmod +x darknet
RUN pip3 list
###########################################
RUN ls /opt/ml/code/
WORKDIR /opt/ml/code
#keep the relevent one below
ENV LD_LIBRARY_PATH=/usr/local/lib:/usr/local/cuda-10.1/targets/x86_64-linux/lib/:/usr/local/cuda-10.1/compat/:$LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH=/usr/local/lib:/usr/local/cuda-11.1.1/targets/x86_64-linux/lib/:/usr/local/cuda-11.1.1/compat/:$LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH=/usr/local/lib:/usr/local/cuda-11.0/targets/x86_64-linux/lib/:/usr/local/cuda-11.0/compat/:$LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH=/usr/local/lib:/usr/local/cuda-10.2/targets/x86_64-linux/lib/:/usr/local/cuda-10.2/compat/:$LD_LIBRARY_PATH
#COPY *.sh /opt/ml/code/
#COPY *.py /opt/ml/code/
#RUN chmod 777 *.sh
######


#ENTRYPOINT ["bash"]
#ENV SAGEMAKER_PROGRAM train.sh
#ENV SAGEMAKER_PROGRAM serve.py