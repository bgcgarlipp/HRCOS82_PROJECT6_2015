#!/usr/bin/env python2

'''
    File name:      processFeatures.py
	Original Author: Emotime
    Update Author:  John Eatwell (35264926)
    Date created:   10/09/2015
    Python Version: 2.7
	Details:        Prepare training sets with labelled features sets for training
	Note:           PvsN parameter was added to distinguish with existing options, 
	                this is used exclusively for AU training 
'''

import cv2
import sys
import os
import itertools
import argparse
import multiprocessing as mp
import datasetConfigParser as dcp
import numpy as np

from string import lower
from os.path import join
from os.path import isfile
from os.path import isdir
from os.path import splitext
from os.path import basename
from os.path import abspath

def lastXFolders(fullpath, x):
    ''' Return last last C parts of a full path '''
    path = fullpath.split( os.sep )
    if (len(path) > (x+1)):
        outPath = []
        for i in range(len(path) - (x + 1), len(path)):
            outPath.append(path[i])
        return os.sep.join(outPath)
    else:
        return fullpath
      
# ------------------------------------- Multiprocessing --------------------------------------------
def initMP(cnt, tlt):
    ''' store the counter for later use '''
    global counter
    global total
    counter = cnt
    total = tlt

def updateProgress():
    global counter
    with counter.get_lock():
        counter.value += 1
    sys.stdout.write("Preparing Training .... [%3d / %3d]\n" %(counter.value, total.value) )
    sys.stdout.flush()
     
def displayProgress(what, item):
    global counter
    global total
    sys.stdout.write("Preparing Training .... [%3d / %3d] Processing (%s): %s \n" %(counter.value, total.value, what, item) )
    sys.stdout.flush()

def callProcess(params):
    """
       Prepare train file with positive and negative samples.
       positive > What you are training for
       negative > What you are not looking for
    """
    (posClass,negClass), dsFolder, config = params
    try:
        displayProgress(posClass, negClass)
        
        updateProgress()
    
        negClass = sorted(negClass)
        posClass = sorted(posClass)
        posPath=[join(dsFolder, join(config['TRAINING_FEATURES'], x)) for x in posClass]
        badPath= [join(dsFolder, join(config['TRAINING_FEATURES'], x)) for x in negClass]
        #
        # Note: a posFolder should contain the filtered images (various orientation and frequency)
        #       of a single sample image. So each line of the training file will be composed by its
        #       MARKER (positive or negative) plus all the pixel values of the filtered images
        #
        posFolders=[]
        for x in posPath:
            posFolders.extend( [join(x, f) for f in os.listdir(x) if isdir(join(x, f)) and f.endswith(config['FILTERED_FOLDER_SUFFIX']) ] )
        posFolders.sort()
    
        negFolders=[]
        for x in badPath:
            negFolders.extend( [join(x, f) for f in os.listdir(x) if isdir(join(x, f)) and f.endswith(config['FILTERED_FOLDER_SUFFIX']) ] )
        negFolders.sort()
    
        outfpath=join( join(dsFolder, config['TRAIN_FOLDER']), "%s_vs_%s%s" % ( '_'.join(posClass), '_'.join(negClass), config['FEATURE_FILE_SUFFIX']) )
    
        sys.stdout.write("Writing details to file: %s\n" %(outfpath))
        sys.stdout.flush()
        
        
        
        with open(outfpath, "w") as tf:
            #
            # POSITIVE SAMPLES
            #
            for fold in posFolders:
                posImgs=[ f for f in os.listdir(fold) if isfile(join(fold, f))]
                posImgs.sort()
                for f in posImgs:
                    fullPath = abspath(join(fold, f))
    #                 displayProgress('P', lastXFolders( fullPath, 2 ))
                    tf.write("P,%s" % fullPath)     # POSITIVE
                tf.write("\n")
            #
            # NEGATIVE SAMPLES
            #
            for fold in negFolders:
                negImgs=[f for f in os.listdir(fold) if isfile(join(fold, f))]
                negImgs.sort()
                for f in negImgs:
                    fullPath = abspath(join(fold, f))
    #                 displayProgress('N', lastXFolders( fullPath, 2 ))
                    tf.write("N,%s" % fullPath)     # POSITIVE
                tf.write("\n")
        return
    except:
        print "Unexpected error:", sys.exc_info()[0]


def multiProcessingTasks(config, tasks):
    # Configure Pooling (with global Counter
    nprocs = max(1, int(mp.cpu_count() * abs(float(config['TRAIN_SVM_CPU_USAGE']))))
    pool = mp.Pool( initializer = initMP, initargs = (mp.Value('i', 0), mp.Value('i', len(tasks))), processes = nprocs )
    
    # Fire up multiprocessing        
    results = []
    pool.map_async(callProcess, tasks, callback = results.append)
    pool.close()
    pool.join()

# --------------------------------------------------------------------------------------------------
def _dataset_multiclass1to1(config):
    ''' Returns a generator of 1 to 1 combinations '''
    for x,y in itertools.combinations( config['CLSLIST'] , 2 ):
        yield ([x],[y])

def _dataset_multiclass1toAllExt(config, ngroups=3):
    """ """
    for z in _dataset_multiclass1toAll(config):
        yield z
    for i in xrange(1, ngroups + 1):
        for z in [ (x, [y for y in config['CLSLIST'] if y not in x]) for x in
            itertools.combinations(config['CLSLIST'], i)]:
            yield z

def _dataset_multiclass1toAll(config):
    """ """
    for z in [ ([x],[y for y in config['CLSLIST'] if y != x]) for x in config['CLSLIST']]:
        yield z

def _dataset_multiclassPvsN(config):
    """ 
        This is specifically for Training of AU.
        Here The AU Features are taken as P and NotAU Features are taken as N
    """
    for x in config["CLSLIST"]:
        yield ([x],["Not{}".format(x)])
    
# --------------------------------------------------------------------------------------------------

def _dataset_load_matrix(filepath):
    """ """
    name,ext=splitext(basename(filepath))
    if ext in ['.yml','.xml']:
        cvmat=cv2.cv.Load(filepath, name=name)
        return np.asarray(cvmat)
    else:
        return cv2.imread(filepath, cv2.CV_LOAD_IMAGE_GRAYSCALE)

def dataset_prepTrainFiles(dsFolder, multiclassMode, config):
    """
        Prepare training files
    """
    bagoftask=[]

    if multiclassMode=='1vs1':
        print "INFO: preparing training files for 1 to 1 multiclass"
        for auCombo in _dataset_multiclass1to1(config):
            bagoftask.append((auCombo, dsFolder, config))

    if multiclassMode=='1vsall':
        print "INFO: preparing training files for 1 to All multiclass"
        for auCombo in _dataset_multiclass1toAll(config):
            bagoftask.append((auCombo, dsFolder, config))
 
    if multiclassMode == '1vsallext':
        print "INFO: preparing training files for 1 to All Extended multiclass"
        for auCombo in _dataset_multiclass1toAllExt(config):
            bagoftask.append((auCombo, dsFolder, config))

    # Added for AU training
    if multiclassMode == 'pvsn':
        print "INFO: preparing training files for 1 to 1 (P vs N)"
        for auCombo in _dataset_multiclassPvsN(config):
            bagoftask.append((auCombo, dsFolder, config))
    
    multiProcessingTasks(config, bagoftask)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cfg", default="dataset.cfg", help="Dataset config file name")
    parser.add_argument("--mode", default="1vsall", choices=['1vs1', '1vsall', '1vsallext', 'pvsn'], help="Training mode for multiclass classification")
    parser.add_argument("dsFolder",help="Dataset base folder")
    args = parser.parse_args()
    try:
        config={}
        config=dcp.parse_ini_config(args.cfg)
        
        dataset_prepTrainFiles(args.dsFolder, lower(args.mode), config)
    except Exception as e:
        print "ERR: something wrong (%s)" % str(e)
        sys.exit(1)
