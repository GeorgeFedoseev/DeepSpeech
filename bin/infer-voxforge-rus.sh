#!/bin/sh
set -xe
if [ ! -f DeepSpeech.py ]; then
    echo "Please make sure you run this from DeepSpeech's top level directory."
    exit 1
fi;



python -u DeepSpeech.py \
  --n_hidden 1024 \
  --checkpoint_dir /assets/network/checkpoint_dir_rus_voxforge_1024/ \
  --one_shot_infer "$@"
