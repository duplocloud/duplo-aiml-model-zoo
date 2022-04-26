ARG BASE_CONTAINER=nvidia/cuda:11.2.2-cudnn8-devel-ubuntu20.04

FROM $BASE_CONTAINER
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests -y gnupg2 ca-certificates git build-essential \
     g++ libopencv-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests -y libsm6 libxext6 libxrender-dev ffmpeg \
    libopencv-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

## ================== python 3.8 =========== todo : move to miniconda
#RUN yum -y install libffi-devel
#RUN yum -y install make gcc openssl-devel bzip2-devel tar
#RUN wget https://www.python.org/ftp/python/3.8.7/Python-3.8.7.tgz
#RUN tar xzf Python-3.8.7.tgz
#WORKDIR /Python-3.8.7
#RUN ./configure --enable-optimizations
#RUN make altinstall
#RUN ln -sfn /usr/local/bin/python3.8 /usr/bin/python3.8
#RUN ln -sfn /usr/local/bin/pip3.8 /usr/bin/pip3.8
#RUN alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 10
#RUN alternatives --install /usr/bin/python python /usr/bin/python2 20
#RUN python3.8 -m pip install -U setuptools
#
#RUN python3 -m pip install --no-cache-dir --upgrade pip \
#    && pip install --no-cache-dir numpy opencv-python
###### v
#RUN pip3 install http://download.pytorch.org/whl/cu90/torch-0.4.0-cp35-cp35m-linux_x86_64.whl --upgrade && \
#    pip3 install torchvision --upgrade
#
#RUN rm -rf /var/lib/apt/lists/*
#RUN rm -rf /root/.cache
#
#ENV PYTHONDONTWRITEBYTECODE=1 \
#    PYTHONUNBUFFERED=1 \
#    LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/local/lib"
## ================== python 3.8 ===========

USER root
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh \
    && echo PATH="/root/miniconda3/bin":$PATH >> .bashrc \
    && exec bash \
    && conda --version

RUN conda --version

#RUN wget https://download.pytorch.org/tutorial/hymenoptera_data.zip
RUN mkdir -p  /root/.local/share/jupyter/kernels
COPY kernels.json /root/.local/share/jupyter/kernels/cnn/

RUN conda update conda
RUN conda create -n cnn python=3.8

# RUN /bin/bash -c "source activate cnn && conda install mkl numpy pandas jupyterl ipython scikit-learn plotly"
RUN /bin/bash -c "source activate cnn && conda install mkl numpy pandas jupyterlab scikit-learn plotly"
RUN /bin/bash -c "source activate cnn && conda install pytorch torchvision -c pytorch"
RUN /bin/bash -c "source activate cnn && conda install -c conda-forge matplotlib opencv seaborn"



CMD ["python3"]

