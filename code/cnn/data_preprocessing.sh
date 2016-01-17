#!/bin/bash
cd data_pre_processing
#python generate_resolution_datasets.py
#python generate_dataset_trainng_test_split_csv.py
python generate_csv.py
cp -r csv/. ../data
