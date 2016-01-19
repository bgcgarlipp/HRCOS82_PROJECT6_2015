#!/bin/bash

# Cleanup
rm -rf ../../dataset

# Preparation
python ../datasetInit.py --cfg dataset_bp_au_24.cfg ../../dataset
python ../datasetFillCsv.py --nomove --cfg dataset_bp_au_24.cfg --csv BP4D-full.csv ../../dataset ../../../databases/BP4D/images ../../../databases/BP4D/aucoding
python ../cropFaces.py --single --cfg dataset_bp_au_24.cfg --eye-correction ../../dataset

# 8 x 8
echo "Training for input image size 8 x 8"
python ../processFeatures.py --cfg dataset_bp_au_8.cfg ../../dataset
python ../processPrepTrain.py --mode pvsn --cfg dataset_bp_au_8.cfg ../../dataset
python ../performTraining.py --mode ada --cfg dataset_bp_au_8.cfg ../../dataset
python ../performVerification.py -v --eye-correction --mode ada --cfg dataset_bp_au_8.cfg ../../dataset

# 16 x 16
echo "Training for input image size 16 x 16"
python ../processFeatures.py --cfg dataset_bp_au_16.cfg ../../dataset
python ../processPrepTrain.py --mode pvsn --cfg dataset_bp_au_16.cfg ../../dataset
python ../performTraining.py --mode svm --cfg dataset_bp_au_16.cfg ../../dataset
python ../performVerification.py -v --eye-correction --mode svm --cfg dataset_bp_au_16.cfg ../../dataset

# 24 x 24
echo "Training for input image size 24 x 24"
python ../processFeatures.py --cfg dataset_bp_au_24.cfg ../../dataset
python ../processPrepTrain.py --mode pvsn --cfg dataset_bp_au_24.cfg ../../dataset
python ../performTraining.py --mode svm --cfg dataset_bp_au_24.cfg ../../dataset
python ../performVerification.py -v --eye-correction --mode svm --cfg dataset_bp_au_24.cfg ../../dataset

# 32 x 32
echo "Training for input image size 32 x 32"
python ../processFeatures.py --cfg dataset_bp_au_32.cfg ../../dataset
python ../processPrepTrain.py --mode pvsn --cfg dataset_bp_au_32.cfg ../../dataset
python ../performTraining.py --mode svm --cfg dataset_bp_au_32.cfg ../../dataset
python ../performVerification.py -v --eye-correction --mode svm --cfg dataset_bp_au_32.cfg ../../dataset

# 40 x 40
echo "Training for input image size 40 x 40"
python ../processFeatures.py --cfg dataset_bp_au_40.cfg ../../dataset
python ../processPrepTrain.py --mode pvsn --cfg dataset_bp_au_40.cfg ../../dataset
python ../performTraining.py --mode svm --cfg dataset_bp_au_40.cfg ../../dataset
python ../performVerification.py -v --eye-correction --mode svm --cfg dataset_bp_au_40.cfg ../../dataset

# 48 x 48
echo "Training for input image size 48 x 48"
python ../processFeatures.py --cfg dataset_bp_au_48.cfg ../../dataset
python ../processPrepTrain.py --mode pvsn --cfg dataset_bp_au_48.cfg ../../dataset
python ../performTraining.py --mode svm --cfg dataset_bp_au_48.cfg ../../dataset
python ../performVerification.py -v --eye-correction --mode svm --cfg dataset_bp_au_48.cfg ../../dataset

# 56 x 56
echo "Training for input image size 56 x 56"
python ../processFeatures.py --cfg dataset_bp_au_56.cfg ../../dataset
python ../processPrepTrain.py --mode pvsn --cfg dataset_bp_au_56.cfg ../../dataset
python ../performTraining.py --mode svm --cfg dataset_bp_au_56.cfg ../../dataset
python ../performVerification.py -v --eye-correction --mode svm --cfg dataset_bp_au_56.cfg ../../dataset