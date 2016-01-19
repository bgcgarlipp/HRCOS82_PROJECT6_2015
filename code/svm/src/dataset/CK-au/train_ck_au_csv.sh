#!/bin/bash

# Cleanup
rm -rf ../../dataset

#Run
python ../datasetInit.py --cfg dataset_ck_au_24.cfg ../../dataset
python ../datasetFillCsv.py --nomove --cfg dataset_ck_au_24.cfg --csv cohn-kanade-images_training_test_split.csv ../../dataset ../../../databases/cohn-kanade/images ../../../databases/cohn-kanade/aucoding
python ../cropFaces.py --single --cfg dataset_ck_au_24.cfg --eye-correction ../../dataset

# 24 x 24
echo "Training for input image size 24 x 24"
python ../processFeatures.py --cfg dataset_ck_au_24.cfg ../../dataset
python ../processPrepTrain.py --mode pvsn --cfg dataset_ck_au_24.cfg ../../dataset
python ../performTraining.py --mode svm --cfg dataset_ck_au_24.cfg ../../dataset
python ../performVerification.py -v --eye-correction --mode svm --cfg dataset_ck_au_24.cfg ../../dataset

# 32 x 32
echo "Training for input image size 32 x 32"
python ../processFeatures.py --cfg dataset_ck_au_32.cfg ../../dataset
python ../processPrepTrain.py --mode pvsn --cfg dataset_ck_au_32.cfg ../../dataset
python ../performTraining.py --single --mode svm --cfg dataset_ck_au_32.cfg ../../dataset
python ../performVerification.py -v --eye-correction --mode svm --cfg dataset_ck_au_32.cfg ../../dataset

# 48 x 48
echo "Training for input image size 48 x 48"
python ../processFeatures.py --cfg dataset_ck_au_48.cfg ../../dataset
python ../processPrepTrain.py --mode pvsn --cfg dataset_ck_au_48.cfg ../../dataset
python ../performTraining.py --single --mode svm --cfg dataset_ck_au_48.cfg ../../dataset
python ../performVerification.py -v --eye-correction --mode svm --cfg dataset_ck_au_48.cfg ../../dataset
