#!/usr/bin/env python2

'''
    File name:      cropFaces.py
    Author:         John Eatwell (35264926)
    Date created:   10/09/2015
    Python Version: 2.7
	Details:        Used in image cropping phase of pre-processing pipeline

'''

import os
import argparse
import datasetConfigParser as dcp
from os.path import join
from os.path import isfile
import multiprocessing as mp
import subprocess

import sys
import timeit


def init(cnt, tlt):
    ''' store the counter for later use '''
    global counter
    global total
    counter = cnt
    total = tlt
    
def callProcess(args):
    param, au = args
    global counter
    global total
    with counter.get_lock():
        counter.value += 1
    sys.stdout.write("Face-Cropping for %s ..................... [%3d / %3d]\r" %(au, counter.value, total.value) )
    sys.stdout.flush()
    retcode=subprocess.call(param, shell=False )
    if retcode==0:
        return (au,True)
    else:
        print""
        print("ERR: %s" % param)
        return (au,False)
    
def multiProcessingTasks(config, tasks):
    # Configure Pooling (with global Counter
    nprocs = max(1, int(mp.cpu_count() * abs(float(config['TRAIN_SVM_CPU_USAGE']))))
    pool = mp.Pool( initializer = init, initargs = (mp.Value('i', 0), mp.Value('i', len(tasks))), processes = nprocs )
    
    # Fire up multiprocessing        
    results = []
    pool.map_async(callProcess, tasks, callback = results.append)
    pool.close()
    pool.join()
    print ""
    
def dataset_cropFaces(dsFolder, config, eye_correction, isSingleThreaded, validation=False):
    """
        Crop faces in dataset
    """
    info = "Starting Face Cropping, "
    if eye_correction:
        info += "with eye correction"
    else:
        info += "without eye correction"
    
    if isSingleThreaded:
        info += " in single threaded mode"
    else:
        info += " in multi-processor mode"

    print info
    
    IMAGES_FOLDER = config['TRAINING_IMAGES']
    FACES_FOLDER = config['TRAINING_FACES']
    
    if validation:
        IMAGES_FOLDER = config['VALIDATION_IMAGES']
        FACES_FOLDER = config['VALIDATION_FACES']
    
    processList = list( config["CLSLIST"] )
    if (config["RECOG_TYPE"].upper() != "EMOTION"):
        for cls in config["CLSLIST"]:
            processList.append("Not{}".format(cls))
    
    # For Emotions, cls = ["neutral", "happy", "sad", ...]
    # For Identity, cls = ["AU1", "NotAU1", "AU2", ...]
    for cls in processList:
        bagoftask = []
        inputPath=join(dsFolder, join(IMAGES_FOLDER, cls))
        outputPath=join(dsFolder, join(FACES_FOLDER, cls))
        
        referenceFilePath = join(inputPath, "images.txt")
        useReferenceFile = False
        if os.path.exists(referenceFilePath):
            imgs = [line.strip() for line in open(referenceFilePath, "r")]
            useReferenceFile = True
        else:
            # Create a list of images to process (if they exist), NOTE THAT IF THERE IS ALREADY A CROPPED IMAGE THEN SKIPPED
            imgs=[ f for f in os.listdir(inputPath) if (isfile(join(inputPath, f)) and not isfile(join(outputPath, f)))]
        
        for i in xrange(0, len(imgs)):
            # Use Haar Cascade features to for facial cropping and eye detection
            cmd = [config['FACECROP_TOOL'], config['FACECROP_FACE_DETECTOR_CFG']]
            if eye_correction:
                cmd.append(config['FACECROP_EYE_DETECTOR_CFG'])

            if useReferenceFile:
                inputImagePath = imgs[i]
            else:
                inputImagePath = join(inputPath, imgs[i])

            cmd.append( str(inputImagePath) )
            
            if useReferenceFile:
                outputImagePath = join(outputPath, os.path.basename(imgs[i])) 
            else:
                outputImagePath = join(outputPath, imgs[i])

            cmd.append( str(outputImagePath) )
            
            if isSingleThreaded:
                sys.stdout.write("Face Cropping for class %4s : .............. (%3d / %3d)\r"%(cls, (i + 1), len(imgs)))
                sys.stdout.flush()
                retcode = subprocess.call(cmd)
                if retcode is not 0:
                    failed+=1
            else:
                bagoftask.append((cmd, cls))
        
        if isSingleThreaded:
            print ""
        
        if not isSingleThreaded:
            # Take tasks and run parallel        
            multiProcessingTasks(config, bagoftask)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cfg", default="dataset.cfg", help="Dataset config file name")
    parser.add_argument("--eye-correction", action="store_true", help="Apply eye correction to faces")
    parser.add_argument("--validation", action="store_true", help="true if it is validation")
    parser.add_argument("--single", action="store_true", help="Use Single Threaded process (slower but better for slow computer)")    
    parser.add_argument("dsFolder", help="Dataset base folder")
    args = parser.parse_args()
    try:
        config={}
        config=dcp.parse_ini_config(args.cfg)

        start_time = timeit.default_timer()
        dataset_cropFaces(args.dsFolder, config, args.eye_correction, args.single, validation=args.validation)
        print "Time Taken: {}".format(timeit.default_timer() - start_time)
    except Exception as e:
        print("ERR: something wrong (%s)" % str(e))
        sys.exit(1)
