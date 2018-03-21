#!/bin/sh
set -xe
if [ ! -f DeepSpeech.py ]; then
    echo "Please make sure you run this from DeepSpeech's top level directory."
    exit 1
fi;



python -u DeepSpeech.py \
  --train_files "/tmp/echo-msk-dataset/echo-msk-train.csv" \
  --dev_files "/tmp/echo-msk-dataset/echo-msk-dev.csv" \
  --test_files "/tmp/echo-msk-dataset/echo-msk-test.csv" \
  --train_batch_size 12 \
  --dev_batch_size 12 \
  --test_batch_size 12 \
  --learning_rate 0.0001 \
  --epoch 30 \
  --display_step 0 \
  --validation_step 5 \
  --dropout_rate 0.30 \
  --default_stddev 0.046875 \
  --n_hidden 1024 \
  --checkpoint_dir /assets/network/checkpoint_dir_echo_msk_1024/ \
  --export_dir /assets/network/export_dir_echo_msk_1024/ \
  --log_level 0 \
  --limit_test 1500 \
  --report_count 100 \
  "$@"
