#!/bin/sh
set -xe
if [ ! -f DeepSpeech.py ]; then
    echo "Please make sure you run this from DeepSpeech's top level directory."
    exit 1
fi;



python -u DeepSpeech.py \
  --n_hidden 2048 \
  --checkpoint_dir /assets/network/yt-vad-1k-then-clean-2048/yt-vad-1k-then-clean-2048-checkpoints/ \
  --one_shot_infer "$@"
