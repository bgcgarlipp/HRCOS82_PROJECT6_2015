#!/usr/bin/env python2
'''
	Use: python createBp4dCsv.py --cfg dataset.cfg --cnt 1010 ../../../databases/BP4D/images ../../../databases/BP4D/aucoding Major_bp4d.csv
'''

import os
import sys
import shutil
import argparse
import datasetConfigParser as dcp
import random
import timeit
import ConfigParser as cp

from random import shuffle
from os.path import isdir
from os.path import isfile
from os.path import join

from auUtils import locateFile
from auUtils import locateFirstFile
from auUtils import isSubSet

from string import strip

class FeraFileInfo():
    def __init__(self):
        self.imageFileRef = "";
        self.presentAU = []
        self.notPresentAU = []
        self.unknownAU = []

def readFERA2015AUCoding(fileName):
    try:
        facsFile = open(fileName, "r")
        feraInfo = []
        descriptors = []
        
        for line in facsFile:
            if (len(line) > 1):
                auDetails = line.replace("\n", "").split(",")

                # First line is a AU descriptor line                
                if len(descriptors) == 0:
                    descriptors = auDetails;
                else:
                    ffInfo = FeraFileInfo()
                    auNumber = 0
                    for field in auDetails:
                        if (auNumber == 0):
                            ffInfo.imageFileRef = field
                        else:
                            # Not present
                            if field == '0':
                                ffInfo.notPresentAU.append(auNumber)
                            # Present
                            elif field == '1':
                                ffInfo.presentAU.append(auNumber)
                            # Unknown
                            elif field == '9':
                                ffInfo.unknownAU.append(auNumber)
                        auNumber += 1
                    feraInfo.append(ffInfo)
#                     print "File:{} Present: {} NotPresent: {} Unknown: {}".format(ffInfo.imageFile, ffInfo.presentAU, ffInfo.notPresentAU, ffInfo.unknownAU)
                
    except IOError as e:
        print "I/O error({0}): reading file {1}".format(e.strerror, fileName)
        return None
    except:
        print "Unexpected error:", sys.exc_info()[0]
    return feraInfo

def findMaxDigits(searchPath):
    fileName = locateFirstFile("*.jpg", searchPath)
    if (fileName == None):
        return 0
    else:
        return len( fileName )
    
def extractImageLimits(config, auList, isTraining):
    limit = -1
    
    try:
        msg = "Training"
        if (isTraining):
            limit = config["RECOG_TRAIN_LIMIT"]
        else:
            limit = config["RECOG_VALIDATE_LIMIT"]
            msg = "Validation"
            
        print "Limiting images for {} per AU: {}".format(msg, limit)    
    except:
        pass

    auLimits = {}
    for au in auList:
        auLimits["AU{}".format(au)] = int(limit)
        auLimits["NotAU{}".format(au)] = int(limit)
    
    return auLimits

# Split list into 2 sets depending on percSplit, which is a whole percentage number (e.g. 80 == 80%)
def chunk(xs, percSplit):
    ys = list(xs)
    random.shuffle(ys)
    random.shuffle(ys)
    random.shuffle(ys)
    groupings = int(len(ys) * percSplit / 100.0 )
    chunks = [ys[n:n+groupings] for n in range(0, len(ys), groupings)]
    return chunks    

def writeOutput(csvFile, training, testing):
    try:
        with open(csvFile, 'w+') as f:
            training.sort()
            for image in training:
                f.write("{},training\n".format(image))
            
            testing.sort()
            for image in testing:
                f.write("{},test\n".format(image))
    except IOError as e:
        print "I/O error({0}): writing file {1}".format(e.strerror, csvFile)
        
def datasetFillFERA2015(imgFolder, labelFolder, config, outputFile, imageCount):
    try:
        imageSplitPercentage = 80   # 80% /20% split
        imageFiles = []
        
        # Note Colon is to create copy and not reference
        auList = [int(x) for x in config["CLASSES"]][:]         
        auNotList = [int(x) for x in config["CLASSES"]][:]
        
        print "Looking for AU: {}".format( auList )
        
        processCount = 0
        for (path, fileName) in locateFile("*.csv", labelFolder):
            if fileName.startswith(tuple(config["SUBJECTS"])):
                processCount += 1
        
        imagesPerLabelFile = (imageCount // processCount) + 1
        imagesPerAu = imageCount // len(auList) * 5
        auLimits = {}
        
        for au in auList:
            auLimits["AU{}".format(au)] = int(imagesPerAu)
            auLimits["NotAU{}".format(au)] = int(imagesPerAu)
        
        for (path, fileName) in locateFile("*.csv", labelFolder):
            info = fileName.replace(".csv", "").split("_")
            subject = info[0]
            shot = info[1]
            imageSearchPath = join(imgFolder, subject, shot)
            
            # Only process subjects 
            if subject in config["SUBJECTS"]:
                print "Processing Subject: {} Task: {}".format(subject, shot)
                facsAuInfo = readFERA2015AUCoding(os.path.join(path, fileName))
                maxLength = findMaxDigits(imageSearchPath)
                
                indexList = [x for x in range(len(facsAuInfo))]
                shuffle(indexList)
                
                cnt = imagesPerLabelFile
                for ind in indexList:
                    if len(imageFiles) >= imageCount:
                        break;
                    
                    auUnknown = [au for au in auList if au in facsAuInfo[ind].unknownAU]
                    
                    if len(auUnknown) == 0:
                        auPresent = [au for au in auList if au in facsAuInfo[ind].presentAU]
                        auNotPresent = [au for au in auNotList if au in facsAuInfo[ind].notPresentAU]
                        
                        if len(auPresent) > 0 or len(auNotPresent) > 0:
                            imageFile = "{}.jpg".format(facsAuInfo[ind].imageFileRef).rjust(maxLength, "0")
                            fileName = "{}/{}/{}".format(subject, shot, imageFile)
                            imageFiles.append(fileName)
                            
                            for au in auPresent:
                                auLimits["AU{}".format(au)] -= 1
                                if auLimits["AU{}".format(au)] == 0:
                                    auList.remove(au)
                                
                            for au in auNotPresent:
                                auLimits["NotAU{}".format(au)] -= 1
                                if auLimits["NotAU{}".format(au)] == 0:
                                    auNotList.remove(au)
                                
                            if len(auList) == 0 and auNotList == 0:
                                auList = config["SEARCH_LIST"][:]
                                auNotList = config["SEARCH_LIST"][:]
                                
                            cnt -= 1
                            if (cnt <= 0):
                                break;
    
        # Split file into training and testing
        trainSplit = chunk(imageFiles, imageSplitPercentage)
        writeOutput(outputFile, trainSplit[0], trainSplit[1])
        
        print "Records written to {}: {} using a {}% split".format(outputFile, len(imageFiles), imageSplitPercentage)
    except Exception as e:
        print("ERR: something wrong (%s)" % str(e))
        
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno) 
        
def parseConfig(configFile):
    config={}
    parser=cp.ConfigParser()
    parser.read(configFile)
    
    clsList = [x for x in parser.get("GENERAL","CLASSES").replace(" ", "").split(',')]
    subjectList = [x for x in parser.get("GENERAL","SUBJECTS").replace(" ", "").split(',')]
    
    config["CLASSES"] = clsList
    config["SUBJECTS"] = subjectList
    
    return config

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cfg", default="bp4f_full.cfg", help="Dataset config file name")
    parser.add_argument("--cnt", dest='cnt', type=int, default=1000, help="Count used")
    parser.add_argument("imgFolder", help="Image database folder")
    parser.add_argument("lblFolder", help="Label folder")
    parser.add_argument("output", help="Output File")
    args = parser.parse_args()
    try:
        config={}
        config=parseConfig(args.cfg)

        start_time = timeit.default_timer()
        datasetFillFERA2015(args.imgFolder, args.lblFolder, config, args.output, args.cnt)
        print "Time Taken: {}".format(timeit.default_timer() - start_time)
    except Exception as e:
        print("ERR: something wrong (%s)" % str(e))
        sys.exit(1)
