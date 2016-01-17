#!/usr/bin/env python2
'''
@author: John Eatwell
'''

import argparse
import sys
import datasetConfigParser as dcp
import os
import subprocess
import re

from subprocess import PIPE

def doPrediction(dsfolder, config, mode, eye_detection, image):
    try:
        if mode == 'svm':
            class_dir = os.path.join(dsfolder, config['CLASSIFIER_SVM_FOLDER'])
        else:
            class_dir = os.path.join(dsfolder, config['CLASSIFIER_ADA_FOLDER'])
    
        execut = config['DETECTION_TOOL']
    
        classificators = []
        for f in os.listdir(class_dir):
            abs_f = os.path.join(class_dir, f)
            if os.path.isfile(abs_f):
                classificators.append(abs_f)
    
        args = [execut, mode, config['FACECROP_FACE_DETECTOR_CFG']]
        if eye_detection:
            args.append(config['FACECROP_EYE_DETECTOR_CFG'])
        else:
            args.append('none')
        args += [config['SIZE']['width'], config['SIZE']['height'],
            config['GABOR_NWIDTHS'], config['GABOR_NLAMBDAS'],
            config['GABOR_NTHETAS']] + classificators
    
        
        res_reg = re.compile("Input File: (.*) Predicted Values: (.*) Finished Prediction")
        faces = '\n'.join(["{}".format(image)])
        
        p = subprocess.Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        out = p.communicate(input=faces)
        
        
        result = re.findall(res_reg, out[0])
        print result[0][1]
    except Exception as  e:
        print "ERR: something wrong (%s) line number " % str(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)        
        sys.exit(1)
        
if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("image", help="Image to process")
#     args = parser.parse_args()

    # Hard coded attributes
    dsFolder = "./predictAU/classifierData"
    cfg = "dataset_parse_au.cfg"
    mode = "svm"
    eye_correction = True
    image="./predictAU/image.jpg"

    try:
        config = {}
        config = dcp.parse_ini_config(cfg)
        doPrediction(dsFolder, config, mode, eye_correction, image)
    except Exception as  e:
        print "ERR: something wrong (%s) line number " % str(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)        
        sys.exit(1)
