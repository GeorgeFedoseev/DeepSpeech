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
  --train_batch_size 12 \
  --dev_batch_size 12 \
  --test_batch_size 12 \
  --learning_rate 0.0001 \
  --epoch 2 \
  --display_step 5 \
  --validation_step 5 \
  --dropout_rate 0.30 \
  --default_stddev 0.046875 \
  --n_hidden 1024 \
  --checkpoint_dir /assets/network/checkpoint_dir_rus_voxforge_1024/ \
  --export_dir /root/assets/network/export_dir_rus_voxforge_1024/ \
  --log_level 0 \
  "$@"
