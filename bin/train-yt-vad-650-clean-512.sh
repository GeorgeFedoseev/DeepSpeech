#!/bin/sh
set -xe
if [ ! -f DeepSpeech.py ]; then
    echo "Please make sure you run this from DeepSpeech's top level directory."
    exit 1
fi;



python -u DeepSpeech.py \
  --train_files "/tmp/yt-vad-650-clean/yt-vad-650-clean-train.csv" \
  --dev_files "/tmp/yt-vad-650-clean/yt-vad-650-clean-dev.csv" \
  --test_files "/tmp/yt-vad-650-clean/yt-vad-650-clean-test.csv" \
  --train_batch_size 12 \
  --dev_batch_size 12 \
  --test_batch_size 12 \
  --learning_rate 0.0001 \
  --epoch 35 \
  --display_step 0 \
  --validation_step 1 \
  --dropout_rate 0.3 \
  --default_stddev 0.046875 \
  --n_hidden 512 \
  --checkpoint_dir /assets/network/yt-vad-650-clean-512/yt-vad-650-clean-512-checkpoints/ \
  --export_dir /assets/network/yt-vad-650-clean-512/yt-vad-650-clean-512-export/ \
  --log_level 1 \
  --report_count 100 \
  --xla=False \
  --use_warpctc=True \
  --log_telegram=True \
  "$@"
