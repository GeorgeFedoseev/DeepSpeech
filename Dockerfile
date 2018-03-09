FROM nvidia/cuda:9.0-cudnn7-runtime-ubuntu16.04

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        wget \
        git \
        python \
        python-dev \
        libcurl3-dev  \
        ca-certificates \
        gcc \
        sox \
        libsox-fmt-mp3 \
        htop \
        nano \
        swig




RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    rm get-pip.py

COPY . /DeepSpeech/

WORKDIR /DeepSpeech

RUN pip --no-cache-dir install -r requirements.txt


RUN python util/taskcluster.py --target /DeepSpeech/native_client/ --arch gpu

# install python bindings
RUN pip install deepspeech