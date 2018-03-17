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
RUN mkdir lm && cd lm && git clone https://github.com/kpu/kenlm && cd kenlm \
    && export EIGEN3_ROOT=/DeepSpeech/data/lm/kenlm/eigen3 \
    && cd $EIGEN3_ROOT && wget -O - https://bitbucket.org/eigen/eigen/get/3.2.8.tar.bz2 |tar xj) && cd - \
    && mkdir -p build \
    && cd build \
    && cmake .. \
    && make -j 4

WORKDIR /DeepSpeech
