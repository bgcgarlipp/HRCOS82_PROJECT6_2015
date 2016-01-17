#!/usr/bin/env python2
"""
   Train with Adaboost and select relevant features
"""
import argparse
import sys
import os
import subprocess
import multiprocessing as mp
import datasetConfigParser as dcp
import timeit

from string import lower
from os.path import join

# ------------------------------------- Multiprocessing --------------------------------------------
def initMP(cnt, tlt):
    ''' Counters for progress '''
    global counter
    global total
    counter = cnt
    total = tlt

def updateProgress():
    global counter
    with counter.get_lock():
        counter.value += 1
    sys.stdout.write("perform Training .... [%3d / %3d]\r" %(counter.value, total.value) )
    sys.stdout.flush()
    
def callProcess(args):
    param, processName = args
    retcode=subprocess.call( param, shell=False )
    updateProgress()
    
    if retcode == 0:
        return (processName,True)
    else:
        print("ERR: '%s' has encountered problems" %processName)
        print "ERR_CALL: {}".format(' '.join(param))
        return (processName,False)

def multiProcessingTasks(config, tasks):
    # Configure Pooling (with global Counter
    nprocs = max(1, int(mp.cpu_count() * abs(float(config['TRAIN_SVM_CPU_USAGE']))))
    pool = mp.Pool( initializer = initMP, initargs = (mp.Value('i', 0), mp.Value('i', len(tasks))), processes = nprocs )
     
    # Fire up multiprocessing        
    results = []
    
    # without .get(2**32) process seems to run to standstill
    pool.map_async(callProcess, tasks, callback = results.append).get(2**32) # workaround for properly handling SIGINT
    pool.close()
    pool.join()
    print ""
    return results
    
# ------------------------------------- -------------- --------------------------------------------

def runTraining(smode, trainFolder, outFolder, config, isSingleThreaded):
    """
        Train svm classifiers
    """
    
    bagoftask = []
    if isSingleThreaded:
        print("INFO: starting training in Single Threaded Mode")
    else:
        print("INFO: starting training in multi-processor mode")
        
    trainCount = len([name for name in os.listdir(trainFolder)])
    currentCount = 1
    
    for trainFile in os.listdir(trainFolder):
        outFile = os.path.splitext(trainFile)[0] + '.xml'
        
        if isSingleThreaded:
            
            sys.stdout.write("perform Training .... [%3d / %3d]\r" %(currentCount, trainCount) )
            sys.stdout.flush()
            
            cmd = [config['TRAIN_TOOL'], smode, '{0}'.format(join(trainFolder, trainFile)), '{0}'.format(join(outFolder, outFile))]
            retcode = subprocess.call(cmd)
            if retcode != 0:
                print("ERR: '%s' has encountered problems" %trainFile)
                print "ERR_CALL: {}".format(' '.join(cmd))
        else:
            bagoftask.append(([config['TRAIN_TOOL'], smode, '{0}'.format(join(trainFolder,
            trainFile)), '{0}'.format(join(outFolder, outFile))], os.path.splitext(trainFile)[0]))
    
        currentCount += 1
    
    # Run Multiprocessing if required
    if not isSingleThreaded:
        results = multiProcessingTasks(config, bagoftask)
    
    print "INFO: {} training finished.".format(smode)
    return results

def initializeTraining(dsFolder, config, mode, isSingleThreaded):
    """
        Start training
    """
    trainFldr = join(dsFolder, config['TRAIN_FOLDER'])
    if mode == "ada":
        smode = "ada"
        classifFldr = join(dsFolder, config['CLASSIFIER_ADA_FOLDER'])
    else:
        smode = "svm"
        classifFldr = join(dsFolder, config['CLASSIFIER_SVM_FOLDER'])
        
    runTraining(smode, trainFldr, classifFldr, config, isSingleThreaded)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cfg", default="dataset.cfg", help="Dataset config file name")
    parser.add_argument("dsFolder", help="Dataset base folder")
    parser.add_argument("--mode", default="svm", choices=['ada', 'svm'], help="training mode: ada (AdaBoost) or svm")
    parser.add_argument("--single", action="store_true", help="Use Single Threaded process (slower but better for slow computer)")
    args = parser.parse_args()

    try:
        # Parse Configuration
        config={}
        config=dcp.parse_ini_config(args.cfg)
        
        # Train for AU
        start_time = timeit.default_timer()
        initializeTraining(args.dsFolder, config, lower(args.mode), args.single)
        print "Training Time Taken: {}".format(timeit.default_timer() - start_time)
    except Exception as e:
        print("ERR: something wrong (%s)" % str(e))
        sys.exit(1)
