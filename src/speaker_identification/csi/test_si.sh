#!/bin/bash
export PYTHONIOENCODING=UTF-8
export BERT_DIR=C:/Users/16013/.cache/modelscope/hub/iic/chinese-roberta-wwm-ext-large # set your model dir
export OUTPUT_DIR=output
export INPUT_DATA=data/WP2021
export MRC_DIR=pretrained/checkpoint_score_f1-97.58_em-97.062.pth  # set your fine-tuned model path

python run_si.py \
  --gpu_ids 0 \
  --n_batch 64 \
  --train_dir $INPUT_DATA/train_features_roberta512.json \
  --dev_dir1 $INPUT_DATA/dev_examples_roberta512.json \
  --dev_dir2 $INPUT_DATA/dev_features_roberta512.json \
  --train_file $INPUT_DATA/train.json \
  --dev_file $INPUT_DATA/test.json \
  --bert_config_file $BERT_DIR/config.json \
  --vocab_file $BERT_DIR/vocab.txt \
  --init_restore_dir $MRC_DIR \
  --checkpoint_dir $OUTPUT_DIR/prediction \
