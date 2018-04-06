#!/bin/sh
set -xe
if [ ! -f DeepSpeech.py ]; then
    echo "Please make sure you run this from DeepSpeech's top level directory."
    exit 1
fi;



python -u DeepSpeech.py \
  --train_files "/tmp/voxforge_ru/voxforge-train.csv" \
  --dev_files "/tmp/voxforge_ru/voxforge-dev.csv" \
  --test_files "/tmp/voxforge_ru/voxforge-test.csv" \
  --train=False \
  --test_batch_size 12 \
  --n_hidden 1024 \
  --checkpoint_dir /assets/network/checkpoint_dir_yt_subs_rus_1024/ \
  --log_level 0 \
  --limit_train 160000000  \
  --report_count 100 \
  --xla=False \
  --beam_width 2048 \
  --use_warpctc=True \
  --log_telegram=False \
  "$@"
