FROM nvidia/cuda:9.0-cudnn7-runtime-ubuntu16.04

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        wget \
        git \
        python \
        libcurl3-dev 



RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    rm get-pip.py

COPY . /DeepSpeech/

WORKDIR /DeepSpeech

RUN pip --no-cache-dir install -r requirements.txt

RUN pip freeze