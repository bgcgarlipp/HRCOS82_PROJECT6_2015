#!/bin/bash

# Cleanup
#rm -rf ../../dataset

# Preparation
#python ../datasetInit.py --cfg dataset_bp_au_24.cfg ../../dataset
#python ../datasetFillCsv.py --nomove --cfg dataset_bp_au_24.cfg --csv BP4D-full.csv ../../dataset ../../../databases/BP4D/images ../../../databases/BP4D/aucoding
#python ../cropFaces.py --single --cfg dataset_bp_au_24.cfg --eye-correction ../../dataset
#7z a -mmt dataset_BP4D-full.7z ../../dataset

# 2 x 2
#echo "Training for input image size 2 x 2"
#python ../processFeatures.py --cfg dataset_bp_au_2.cfg ../../dataset
#python ../processPrepTrain.py --mode pvsn --cfg dataset_bp_au_2.cfg ../../dataset
#python ../performTraining.py --mode svm --cfg dataset_bp_au_2.cfg ../../dataset
#python ../performVerification.py -v --eye-correction --mode svm --cfg dataset_bp_au_2.cfg ../../dataset
#7z a svm2x2.7z ../../dataset/classifiers/svm

# 4 x 4
#echo "Training for input image size 4 x 4"
#python ../processFeatures.py --cfg dataset_bp_au_4.cfg ../../dataset
#python ../processPrepTrain.py --mode pvsn --cfg dataset_bp_au_4.cfg ../../dataset
#python ../performTraining.py --mode svm --cfg dataset_bp_au_4.cfg ../../dataset
#python ../performVerification.py -v --eye-correction --mode svm --cfg dataset_bp_au_4.cfg ../../dataset
#7z a svm4x4.7z ../../dataset/classifiers/svm

# 8 x 8
echo "Training for input image size 8 x 8"
python ../processFeatures.py --cfg dataset_bp_au_8.cfg ../../dataset
python ../processPrepTrain.py --mode pvsn --cfg dataset_bp_au_8.cfg ../../dataset
python ../performTraining.py --mode ada --cfg dataset_bp_au_8.cfg ../../dataset
python ../performVerification.py -v --eye-correction --mode ada --cfg dataset_bp_au_8.cfg ../../dataset
#7z a svm8x8.7z ../../dataset/classifiers/svm

# 16 x 16
#echo "Training for input image size 16 x 16"
#python ../processFeatures.py --cfg dataset_bp_au_16.cfg ../../dataset
#python ../processPrepTrain.py --mode pvsn --cfg dataset_bp_au_16.cfg ../../dataset
#python ../performTraining.py --mode svm --cfg dataset_bp_au_16.cfg ../../dataset
#python ../performVerification.py -v --eye-correction --mode svm --cfg dataset_bp_au_16.cfg ../../dataset
#7z a svm16x16.7z ../../dataset/classifiers/svm

# 24 x 24
#echo "Training for input image size 24 x 24"
#python ../processFeatures.py --cfg dataset_bp_au_24.cfg ../../dataset
#python ../processPrepTrain.py --mode pvsn --cfg dataset_bp_au_24.cfg ../../dataset
#python ../performTraining.py --mode svm --cfg dataset_bp_au_24.cfg ../../dataset
#python ../performVerification.py -v --eye-correction --mode svm --cfg dataset_bp_au_24.cfg ../../dataset
#7z a svm24x24.7z ../../dataset/classifiers/svm

# 32 x 32
#echo "Training for input image size 32 x 32"
#python ../processFeatures.py --cfg dataset_bp_au_32.cfg ../../dataset
#python ../processPrepTrain.py --mode pvsn --cfg dataset_bp_au_32.cfg ../../dataset
#python ../performTraining.py --mode svm --cfg dataset_bp_au_32.cfg ../../dataset
#python ../performVerification.py -v --eye-correction --mode svm --cfg dataset_bp_au_32.cfg ../../dataset
#7z a svm32x32.7z ../../dataset/classifiers/svm

# 40 x 40
#echo "Training for input image size 40 x 40"
#python ../processFeatures.py --cfg dataset_bp_au_40.cfg ../../dataset
#python ../processPrepTrain.py --mode pvsn --cfg dataset_bp_au_40.cfg ../../dataset
#python ../performTraining.py --mode svm --cfg dataset_bp_au_40.cfg ../../dataset
#python ../performVerification.py -v --eye-correction --mode svm --cfg dataset_bp_au_40.cfg ../../dataset
#7z a svm40x40.7z ../../dataset/classifiers/svm

# 48 x 48
#echo "Training for input image size 48 x 48"
#python ../processFeatures.py --cfg dataset_bp_au_48.cfg ../../dataset
#python ../processPrepTrain.py --mode pvsn --cfg dataset_bp_au_48.cfg ../../dataset
#python ../performTraining.py --mode svm --cfg dataset_bp_au_48.cfg ../../dataset
#python ../performVerification.py -v --eye-correction --mode svm --cfg dataset_bp_au_48.cfg ../../dataset
#7z a svm48x48.7z ../../dataset/classifiers/svm

# 56 x 56
#echo "Training for input image size 56 x 56"
#python ../processFeatures.py --cfg dataset_bp_au_56.cfg ../../dataset
#python ../processPrepTrain.py --mode pvsn --cfg dataset_bp_au_56.cfg ../../dataset
#python ../performTraining.py --mode svm --cfg dataset_bp_au_56.cfg ../../dataset
#python ../performVerification.py -v --eye-correction --mode svm --cfg dataset_bp_au_56.cfg ../../dataset
#7z a svm56x56.7z ../../dataset/classifiers/svm