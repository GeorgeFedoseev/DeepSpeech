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
        swig \
        cmake \
        libboost-all-dev \
        zlib1g-dev \
        libbz2-dev \
        liblzma-dev \
        locales




RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    rm get-pip.py

COPY . /DeepSpeech/

WORKDIR /DeepSpeech

RUN pip --no-cache-dir install -r requirements.txt


RUN python util/taskcluster.py --target /DeepSpeech/native_client/ --arch gpu

# install python bindings
RUN pip install deepspeech

# allow python printing utf-8
ENV PYTHONIOENCODING UTF-8

# build kenlm
WORKDIR /DeepSpeech/data
RUN mkdir lm
RUN git clone https://github.com/kpu/kenlm && cd kenlm
RUN mkdir -p build && cd build && cmake .. && make -j 4

WORKDIR /DeepSpeech
