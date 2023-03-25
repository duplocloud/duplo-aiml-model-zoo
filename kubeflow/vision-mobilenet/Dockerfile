FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8


RUN apt-get update && apt-get install -y \
    python3 \
  python3-pip \
  && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install "/usr/bin/python" "python" "$(which python3)" 1
RUN python -m pip install --upgrade pip

RUN python --version
RUN pip --version

COPY requirements.txt   /requirements.txt
COPY imagedata /data
COPY *.py /code

RUN pip install -r /requirements.txt

ENV MAPPED_PATH="/data"
CMD ["python", "/code/train.py"]