#!/bin/sh
set -xe
if [ ! -f DeepSpeech.py ]; then
    echo "Please make sure you run this from DeepSpeech's top level directory."
    exit 1
fi;



python -u DeepSpeech.py \
  --train_files "/tmp/yt-subs-rus-dataset/yt-subs-train.csv" \
  --dev_files "/tmp/yt-subs-rus-dataset/yt-subs-dev.csv" \
  --test_files "/tmp/yt-subs-rus-dataset/yt-subs-test.csv" \
  --train_batch_size 32 \
  --dev_batch_size 16 \
  --test_batch_size 16 \
  --learning_rate 0.0001 \
  --epoch 35 \
  --display_step 0 \
  --validation_step 1 \
  --dropout_rate 0.20 \
  --default_stddev 0.046875 \
  --n_hidden 1024 \
  --checkpoint_dir /assets/network/checkpoint_dir_yt_subs_rus_1024/ \
  --export_dir /assets/network/export_dir_yt_subs_rus_1024/ \
  --log_level 1 \
  --limit_train 160000000  \
  --report_count 100 \
  --xla=False \
  --use_warpctc=True \
  --log_telegram=True \
  "$@"
