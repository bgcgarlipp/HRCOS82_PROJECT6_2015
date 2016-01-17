#!/usr/bin/env python2
"""
  Calculate Gabor features features
"""
import os
import argparse
import datasetConfigParser as dcp
import sys

import multiprocessing as mp
import subprocess

from os.path import join
from os.path import isfile
import timeit

def init(cnt, tlt):
    ''' store the counter for later use '''
    global counter
    global total
    counter = cnt
    total = tlt
    
def callProcess(args):
    param, comstr, au = args
    global counter
    global total
    with counter.get_lock():
        counter.value += 1
    sys.stdout.write("Extracting features for %s ............... [%3d / %3d]\r" %(au, counter.value, total.value))
    sys.stdout.flush()
    retcode=subprocess.call(param, shell=False )
    if retcode==0:
        return (comstr,True)
    else:
        print""
        print("ERR: '%s' has encountered problems" % comstr)
        return (comstr,False)
               
def calcFeatures(dsFolder, config, validation=False):
    """ Calculate features on dataset"""
#     print("INFO: calculating gabor features")
    calcGaborBank(dsFolder,config, validation=validation)


def calcGaborBank(dsFolder, config, validation=False):
    """
        Calculate features using a gabor filters bank
    """
    FACES_FOLDER = config['TRAINING_FACES']
    FEATURES_FOLDER = config['TRAINING_FEATURES']
    if validation:
        FACES_FOLDER = config['VALIDATION_FACES']
        FEATURES_FOLDER = config['VALIDATION_FEATURES']

    # Emotion and AU Identity lists are different
    processList = list( config["CLSLIST"] )
    if (config["RECOG_TYPE"].upper() != "EMOTION"):
        for cls in config["CLSLIST"]:
            processList.append("Not{}".format(cls))

        
    for cls in processList:
        bagoftask = []
        facesFolder=join(dsFolder, join(FACES_FOLDER, cls))
        featsFolder=join(dsFolder, join(FEATURES_FOLDER, cls))
        faces=[ f for f in os.listdir(facesFolder) if isfile(join(facesFolder, f))]
        _NJOBS = len(faces)
        for i in xrange(0, len(faces)):
            face = faces[i]
            faceFile=join(facesFolder, face)
            featFolder=join(featsFolder, os.path.splitext(face)[0]) + config['FILTERED_FOLDER_SUFFIX']
            try:
                os.mkdir(featFolder)
            except Exception:
                pass

            featFile=join(featFolder, config['GABOR_FEAT_FNAME'])
            cmd=[config['GABOR_TOOL'], 
                 str(config['SIZE']['width']), str(config['SIZE']['height']),
                 config['GABOR_NWIDTHS'], config['GABOR_NLAMBDAS'], config['GABOR_NTHETAS'],
                 str(faceFile), str(featFile)]
#             if 'GABOR_FILTER_FILE' in config.keys():
#                 if config['GABOR_FILTER_FILE'] != 'NA':
#                     cmd.append(config['GABOR_FILTER_FILE'])

            bagoftask.append((cmd,'GaborFilter {0}'.format(faceFile),cls))
                
        # Configure Pooling (with global Counter
        nprocs = max(1, int(mp.cpu_count() * abs(float(config['TRAIN_SVM_CPU_USAGE']))))
        pool = mp.Pool( initializer = init, initargs = (mp.Value('i', 0), mp.Value('i', len(bagoftask))), processes = nprocs )

        # Fire up multiprocessing        
        results = []
        pool.map_async(callProcess, bagoftask, callback = results.append)
        pool.close()
        pool.join()
        print ""
          
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cfg", default="dataset.cfg", help="Dataset config file name")
    parser.add_argument("--validation", action="store_true", help="true if it is validation")
    parser.add_argument("dsFolder", help="Dataset base folder")
    args = parser.parse_args()
    try:
        config={}
        config=dcp.parse_ini_config(args.cfg)
        
        start_time = timeit.default_timer()
        calcFeatures(args.dsFolder, config, validation=args.validation)
        print "Time Taken: {}".format(timeit.default_timer() - start_time)
    except Exception as e:
        print("ERR: something wrong (%s)" % str(e))
        sys.exit(1)
