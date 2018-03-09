FROM nvidia/cuda:9.0-cudnn7-runtime-ubuntu16.04

WORKDIR ~/

RUN nvidia-smi