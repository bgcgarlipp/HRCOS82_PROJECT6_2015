#!/bin/bash

# Cleanup
#rm -rf ../../dataset

# Preparation
#python ../datasetInit.py --cfg dataset_bp_au_24.cfg ../../dataset
#python ../datasetFillCsv.py --nomove --cfg dataset_bp_au_24.cfg --csv BP4D-female.csv ../../dataset ../../../databases/BP4D/images ../../../databases/BP4D/aucoding
#python ../cropFaces.py --single --cfg dataset_bp_au_24.cfg --eye-correction ../../dataset
#7z a -mmt dataset_BP4D-female.7z ../../dataset

# 24 x 24
echo "Training for input image size 24 x 24"
python ../processFeatures.py --cfg dataset_bp_au_24.cfg ../../dataset
python ../processPrepTrain.py --mode pvsn --cfg dataset_bp_au_24.cfg ../../dataset
python ../performTraining.py --mode svm --cfg dataset_bp_au_24.cfg ../../dataset
python ../performVerification.py -v --eye-correction --mode svm --cfg dataset_bp_au_24.cfg ../../dataset
7z a svm24x24.7z ../../dataset/classifiers/svm

# 32 x 32
echo "Training for input image size 32 x 32"
python ../processFeatures.py --cfg dataset_bp_au_32.cfg ../../dataset
python ../processPrepTrain.py --mode pvsn --cfg dataset_bp_au_32.cfg ../../dataset
python ../performTraining.py --mode svm --cfg dataset_bp_au_32.cfg ../../dataset
python ../performVerification.py -v --eye-correction --mode svm --cfg dataset_bp_au_32.cfg ../../dataset
7z a svm32x32.7z ../../dataset/classifiers/svm

# 48 x 48
echo "Training for input image size 48 x 48"
python ../processFeatures.py --cfg dataset_bp_au_48.cfg ../../dataset
python ../processPrepTrain.py --mode pvsn --cfg dataset_bp_au_48.cfg ../../dataset
python ../performTraining.py --mode svm --cfg dataset_bp_au_48.cfg ../../dataset
python ../performVerification.py -v --eye-correction --mode svm --cfg dataset_bp_au_48.cfg ../../dataset
7z a svm48x48.7z ../../dataset/classifiers/svm
