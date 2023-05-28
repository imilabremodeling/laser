#!/bin/bash
number_of_training=1

while true ; do
  echo "正要開始第 $number_of_training 輪預測"
  python3 /home/jovyan/predict-code/inference.py
  number_of_training=$((number_of_training+1))
  sleep 10s
  
done
