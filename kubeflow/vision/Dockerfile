FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8

RUN apt-get update -y \
apt-get install -y --no-install-recommends python3.8 curl \
apt-get clean \
rm -rf /var/lib/apt/lists/*

COPY requirements.txt /requirements.txt
COPY data /data
COPY *.py /code

RUN python3 -m pip install --no-cache-dir -r /requirements.txt -U

ENV MAPPED_PATH="/data"
CMD ["python", "/code/train.py"]