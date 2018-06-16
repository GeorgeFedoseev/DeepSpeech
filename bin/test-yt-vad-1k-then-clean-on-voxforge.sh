#!/bin/sh
set -xe
if [ ! -f DeepSpeech.py ]; then
    echo "Please make sure you run this from DeepSpeech's top level directory."
    exit 1
fi;



python -u DeepSpeech.py \
  --train=0 \
  --train_files "/datasets/voxforge-ru-clean/voxforge-ru-clean-train.csv" \
  --dev_files "/datasets/voxforge-ru-clean/voxforge-ru-clean-dev.csv" \
  --test_files "/datasets/voxforge-ru-clean/voxforge-ru-clean-test.csv" \
  --train_batch_size 32 \
  --dev_batch_size 16 \
  --test_batch_size 16 \
  --learning_rate 0.0001 \
  --epoch 35 \
  --display_step 0 \
  --validation_step 1 \
  --dropout_rate 0.3 \
  --default_stddev 0.046875 \
  --n_hidden 2048 \
  --checkpoint_dir /assets/network/yt-vad-1k-then-clean-2048/yt-vad-1k-then-clean-2048-checkpoints/ \
  --export_dir /assets/network/yt-vad-1k-then-clean-2048/yt-vad-1k-then-clean-2048-export/ \
  --log_level 1 \
  --report_count 100 \
  --xla=False \
  --use_warpctc=True \
  --log_telegram=True \
  "$@"
