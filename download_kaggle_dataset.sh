#!/bin/bash
kaggle datasets download -d $DATASET_NAME
unzip -o -p $DATASET_NAME > dataset.csv 
mkdir datasets/ && mv dataset.csv datasets/