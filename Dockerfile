FROM nvidia/cuda:9.0-cudnn7-devel-ubuntu16.04

RUN cp /usr/include/cudnn.h /usr/local/cuda/include/cudnn.h

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        wget \
        git \
        python \
        python-dev \
        python-pip \
        python-wheel \
        python-numpy \
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


# BUILD TensoFlow from Mozilla repo with XLA-AOT



RUN git clone https://github.com/mozilla/tensorflow/
WORKDIR /tensorflow
RUN git checkout r1.6



# install Bazel
RUN apt-get install -y openjdk-8-jdk
RUN echo "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list
RUN curl https://bazel.build/bazel-release.pub.gpg | apt-key add -
RUN apt-get update && apt-get install -y bazel


# install GPU stuff
RUN apt-get install -y cuda-command-line-tools-9-0 
RUN export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/extras/CUPTI/lib64

# configure Tensorflow Build

# GPU Environment Setup
ENV TF_NEED_CUDA 1
ENV CUDA_TOOLKIT_PATH /usr/local/cuda
ENV CUDA_PKG_VERSION 9-0=9.0.176-1
ENV CUDA_VERSION 9.0.176
ENV TF_CUDA_VERSION 9.0
ENV TF_CUDNN_VERSION 7.1.1.5
ENV CUDNN_INSTALL_PATH /usr/local/cuda
ENV TF_CUDA_COMPUTE_CAPABILITIES 6

# Common Environment Setup
ENV TF_BUILD_CONTAINER_TYPE GPU
ENV TF_BUILD_OPTIONS OPT
ENV TF_BUILD_DISABLE_GCP 1
ENV TF_BUILD_ENABLE_XLA 1
ENV TF_BUILD_PYTHON_VERSION PYTHON2
ENV TF_BUILD_IS_OPT OPT
ENV TF_BUILD_IS_PIP PIP

# Other Parameters
ENV CC_OPT_FLAGS -mavx -mavx2 -msse4.1 -msse4.2 -mfma
ENV TF_NEED_GCP 0
ENV TF_NEED_HDFS 0
ENV TF_NEED_JEMALLOC 1
ENV TF_NEED_OPENCL 0
ENV TF_CUDA_CLANG 0
ENV TF_NEED_MKL 0
ENV TF_ENABLE_XLA 1
ENV PYTHON_BIN_PATH /usr/bin/python2.7
ENV PYTHON_LIB_PATH /usr/lib/python2.7/dist-packages



# link DeepSpeech native_client libs to tf folder
COPY . /DeepSpeech/
RUN ln -s /DeepSpeech/native_client ./

#RUN bazel build -c opt --copt=-O3 //native_client:libctc_decoder_with_kenlm.so
#RUN bazel build --config=monolithic -c opt --copt=-O3 --copt=-fvisibility=hidden --define=DS_NATIVE_MODEL=1 --define=DS_MODEL_TIMESTEPS=64 --define=DS_MODEL_FRAMESIZE=494 --define=DS_MODEL_FILE=/tmp/model.ldc93s1.pb //native_client:libdeepspeech_model.so //native_client:libdeepspeech.so //native_client:deepspeech_utils //native_client:generate_trie
