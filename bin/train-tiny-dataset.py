#!/bin/sh
set -xe
if [ ! -f DeepSpeech.py ]; then
    echo "Please make sure you run this from DeepSpeech's top level directory."
    exit 1
fi;



python -u DeepSpeech.py \
  --train_files "/DeepSpeech/data/tiny-dataset/tiny-train.csv" \
  --dev_files "/DeepSpeech/data/tiny-dataset/tiny-dev.csv" \
  --test_files "/DeepSpeech/data/tiny-dataset/tiny-test.csv" \
  --train_batch_size 1 \
  --dev_batch_size 1 \
  --test_batch_size 1 \
  --learning_rate 0.0001 \
  --epoch 35 \
  --display_step 0 \
  --validation_step 1 \
  --dropout_rate 0.3 \
  --default_stddev 0.046875 \
  --n_hidden 512 \
  --checkpoint_dir /network/tiny-dataset-512/tiny-dataset-512-checkpoints/ \
  --export_dir /network/tiny-dataset-512/tiny-dataset-512-2048-export/ \
  --log_level 1 \
  --report_count 3 \
  --xla=False \
  --use_warpctc=True \
  --log_telegram=True \
  "$@"
