#!/bin/bash

# Cleanup
rm -rf ../../dataset

#Run (input image size does not matter)
python ../datasetInit.py --cfg dataset_ck_emo_24.cfg ../../dataset
python ../datasetFillCsv.py --nomove --cfg dataset_ck_emo_24.cfg --csv CKEmoTrain.csv ../../dataset ../../../databases/cohn-kanade/images ../../../databases/cohn-kanade/emotions
python ../cropFaces.py --single --cfg dataset_ck_emo_24.cfg --eye-correction ../../dataset

# 24 x 24
echo "Training for input image size 24 x 24"
python ../processFeatures.py --cfg dataset_ck_emo_24.cfg ../../dataset
python ../processPrepTrain.py --mode 1vsall --cfg dataset_ck_emo_24.cfg ../../dataset
python ../performTraining.py --mode svm --cfg dataset_ck_emo_24.cfg ../../dataset
python ../performVerification.py -v --eye-correction --mode svm --cfg dataset_ck_emo_24.cfg ../../dataset

# 32 x 32
echo "Training for input image size 32 x 32"
python ../processFeatures.py --cfg dataset_ck_emo_32.cfg ../../dataset
python ../processPrepTrain.py --mode 1vsall --cfg dataset_ck_emo_32.cfg ../../dataset
python ../performTraining.py --mode svm --cfg dataset_ck_emo_32.cfg ../../dataset
python ../performVerification.py -v --eye-correction --mode svm --cfg dataset_ck_emo_32.cfg ../../dataset

# 48 x 48
echo "Training for input image size 48 x 48"
python ../processFeatures.py --cfg dataset_ck_emo_48.cfg ../../dataset
python ../processPrepTrain.py --mode 1vsall --cfg dataset_ck_emo_48.cfg ../../dataset
python ../performTraining.py --mode svm --cfg dataset_ck_emo_48.cfg ../../dataset
python ../performVerification.py -v --eye-correction --mode svm --cfg dataset_ck_emo_48.cfg ../../dataset
