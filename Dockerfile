# Need devel version cause we need /usr/include/cudnn.h 
# for compiling libctc_decoder_with_kenlm.so
FROM nvidia/cuda:9.0-cudnn7-devel-ubuntu16.04



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
        gcc-4.8 \
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


# <BUILD TensorFlow+XLA
# build TensoFlow from Mozilla repo with XLA


RUN git clone https://github.com/mozilla/tensorflow/
WORKDIR /tensorflow
RUN git checkout r1.6



# install Bazel
RUN apt-get install -y openjdk-8-jdk
RUN echo "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list
RUN curl https://bazel.build/bazel-release.pub.gpg | apt-key add -
RUN apt-get update && apt-get install -y bazel && apt-get upgrade -y bazel


# install GPU stuff
RUN apt-get install -y cuda-command-line-tools-9-0 


# configure Tensorflow Build

# GPU Environment Setup
ENV TF_NEED_CUDA 1
ENV CUDA_TOOLKIT_PATH /usr/local/cuda
ENV CUDA_PKG_VERSION 9-0=9.0.176-1
ENV CUDA_VERSION 9.0.176
ENV TF_CUDA_VERSION 9.0
ENV TF_CUDNN_VERSION 7.1.1
ENV CUDNN_INSTALL_PATH /usr/lib/x86_64-linux-gnu/
ENV TF_CUDA_COMPUTE_CAPABILITIES 6.0

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

RUN ln -s /DeepSpeech/native_client /tensorflow

WORKDIR /DeepSpeech

RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    rm get-pip.py

RUN pip --no-cache-dir install -r requirements.txt
RUN python util/taskcluster.py --target /DeepSpeech/native_client/ --arch gpu

WORKDIR /tensorflow




# Running bazel inside a `docker build` command causes trouble, cf:
#   https://github.com/bazelbuild/bazel/issues/134
# The easiest solution is to set up a bazelrc file forcing --batch.
RUN echo "startup --batch" >>/etc/bazel.bazelrc
# Similarly, we need to workaround sandboxing issues:
#   https://github.com/bazelbuild/bazel/issues/418
RUN echo "build --spawn_strategy=standalone --genrule_strategy=standalone" \
    >>/etc/bazel.bazelrc


# fix for failing bazel TF build
RUN ln -s /usr/local/cuda/lib64/stubs/libcuda.so /usr/local/cuda/lib64/stubs/libcuda.so.1

# fix
RUN cp /usr/include/cudnn.h /usr/local/cuda/include/cudnn.h

ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:/usr/local/cuda/extras/CUPTI/lib64:/usr/local/cuda/lib64:/usr/lib/x86_64-linux-gnu/:/usr/local/cuda/lib64/stubs/

# BUILD
# need add --config=cuda?
RUN bazel build --config=cuda -c opt --copt=-O3 //native_client:libctc_decoder_with_kenlm.so  --verbose_failures --action_env=LD_LIBRARY_PATH=${LD_LIBRARY_PATH}

# need add --config=cuda?
RUN bazel build --config=cuda --config=monolithic --config=opt -c opt --copt=-O3 --copt=-fvisibility=hidden //native_client:libdeepspeech.so //native_client:deepspeech_utils //native_client:generate_trie  --verbose_failures --action_env=LD_LIBRARY_PATH=${LD_LIBRARY_PATH}

# passing LD_LIBRARY_PATH is required cause Bazel doesnt pickup it from env
RUN bazel build --config=opt --config=cuda  --copt=-msse4.2 //tensorflow/tools/pip_package:build_pip_package --verbose_failures --action_env=LD_LIBRARY_PATH=${LD_LIBRARY_PATH}

# fix for not found script https://github.com/tensorflow/tensorflow/issues/471
RUN ./configure

# build wheel
RUN bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg

# install tensorflow from our custom wheel
RUN pip install /tmp/tensorflow_pkg/tensorflow_warpctc-1.6.0-cp27-cp27mu-linux_x86_64.whl

# BUILD TensorFlow+XLA />
