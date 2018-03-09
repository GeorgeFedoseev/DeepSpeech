FROM nvidia/cuda

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
        libcurl3-dev 

WORKDIR ~/

RUN nvidia-smi