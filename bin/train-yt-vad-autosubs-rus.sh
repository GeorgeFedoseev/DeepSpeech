#!/bin/sh
set -xe
if [ ! -f DeepSpeech.py ]; then
    echo "Please make sure you run this from DeepSpeech's top level directory."
    exit 1
fi;



python -u DeepSpeech.py \
  --train_files "/tmp/yt-vad-autosubs-dataset/yt-vad-autosubs-train.csv" \
  --dev_files "/tmp/yt-vad-autosubs-dataset/yt-vad-autosubs-dev.csv" \
  --test_files "/tmp/yt-vad-autosubs-dataset/yt-vad-autosubs-test.csv" \
  --train_batch_size 32 \
  --dev_batch_size 16 \
  --test_batch_size 16 \
  --learning_rate 0.0001 \
  --epoch 35 \
  --display_step 0 \
  --validation_step 1 \
  --dropout_rate 0.30 \
  --default_stddev 0.046875 \
  --n_hidden 2500 \
  --checkpoint_dir /assets/network/yt-vad-autosubs-2500/yt-vad-autosubs-2500-checkpoints/ \
  --export_dir /assets/network/yt-vad-autosubs-2500/yt-vad-autosubs-2500-export/ \
  --log_level 1 \
  --report_count 100 \
  --xla=False \
  --use_warpctc=True \
  --log_telegram=True \
  "$@"
