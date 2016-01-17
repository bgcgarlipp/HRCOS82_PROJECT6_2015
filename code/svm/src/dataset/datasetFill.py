#!/usr/bin/env python2
"""
  Import the Chon-Kanade plus database to a dataset.
"""
import os
import sys
import shutil
import argparse
import datasetConfigParser as dcp
import random
import timeit

from os.path import isdir
from os.path import isfile
from os.path import join

from auUtils import locateFile
from auUtils import locateFirstFile
from auUtils import isSubSet

from string import strip

# ----------------------------------- CK+ Specific Information
def readFACSFile(fileName):
    """
        Read in FACS information and return array
        fileName:  Full File Path
        RETURN:    Array of [au, intensity]
    """
    details = []
    try:
        facsFile = open(fileName, "r")
        for line in facsFile:
            if (len(line) > 1):
                auDetails = line.split()
                au = int(float(auDetails[0]))
                intensity = (int(float(auDetails[1])))
                details.append([au, intensity])
    except IOError as e:
        print "I/O error({0}): reading file {1}".format(e.strerror, fileName)
        return None
    except:
        print "Unexpected error:", sys.exc_info()[0]
    return details

def readCkEmoFile(emolist, fileName, subject, shot):
    emo="None"
    try:
        emoFile = open(fileName, "r")
        line = emoFile.read()
        
        if len(line)==0:
            print "WARN: subject {} shot {} has void emo label File:'{}', (skipping!)".format(subject, shot, fileName)
                # A label file could be void, in this case skip the current shot
        else:
            emoNum = int(float(strip(line)))
            emo = emolist[emoNum]
        emoFile.close()
    except IOError as e:
        print "I/O error({0}): reading file {1}".format(e.strerror, fileName)
        return None
    except:
        print "ERROR: cannot parse emotional label for subject {} shot {} File:{}, (skipping!)".format(subject, shot, fileName)
    return emo

def copyImageFile(source, destination):
    try:
        shutil.copy(source, destination)
    except IOError as err:
        if not isfile(source):
            print "ERR: cannot copy image {0} > FILE DOES NOT EXIST".format(source)
        else:
            print "ERR: cannot copy image {0} to dataset {1} Reason: {2}".format(source, destination, err.strerror)

def writeValidationData(imageFileName, data, isAU):
    validationDataFile = imageFileName
    try:
        validationDataFile = "{}.txt".format( imageFileName[:-4] )
        dataFile = open(validationDataFile, "w")
        for info in data:
            if isAU:
                dataFile.write( "AU{}\n".format(info) )
            else:
                dataFile.write( "{}\n".format(info) )
        dataFile.close()
    except IOError as e:
        print "I/O error({0}): writing file {1}".format(e.strerror, validationDataFile)

    
def dataset_fillCohnKanade(dsFolder, imgFolder, labelFolder, config, vperc=0.3, vseed=0):
    """
        Fill dataset with Cohn Kanade + data.
        Note: List of AU to recognize in config["CLSLIST"]
    """
    
    lookingForEmotion = False
    if (config["RECOG_TYPE"].upper() == "EMOTION"):
        lookingForEmotion = True

    if lookingForEmotion:
        print "Looking for the following Emotions: {0}".format( config["CLSLIST"] )
    else:
        print "Looking for the following AU: {0}".format( config["CLSLIST"] )
    
    # First extract a folders in Cohn Kanade database
    subjects = [ x for x in os.listdir(imgFolder) if isdir(join(imgFolder, x)) ]
    print "INFO: %d subjects found in CK+ database" % len(subjects)
    subjects.sort()

    for subject in subjects:
        print "INFO: Processing subject %s" % subject

        labelFolders = [x for x in os.listdir(join(labelFolder, subject)) if isdir(join(labelFolder, join(subject, x)))]
        imageFolders = [x for x in os.listdir(join(imgFolder, subject)) if isdir(join(labelFolder, join(subject, x)))]

        shots = [x for x in imageFolders if x in labelFolders]
        shots.sort()
        for shot in shots:
            #print "INFO: Processing shot %shot " % shot

            pics = [x for x in os.listdir(join(imgFolder, join(subject, shot))) if isfile(join(imgFolder, join(subject, join(shot, x))))]
            pics.sort()
            labels = [x for x in os.listdir(join(labelFolder, join(subject, shot))) if isfile(join(labelFolder, join(subject, join(shot, x)))) ]
            
            if len(labels) < 1 or len(pics) < 1:
                # label folder could contain no file at all, in this case skip the current shot or mark it as neutral?
#                 print "WARN: subject %s shot %s has #%d emo labels and #%d pictures, (skip:incomplete)" % (subject, shot, len(labels), len(pics))
                continue
 
            dataFile = join(labelFolder, join(subject, join(shot, labels[0])))
            
            training = True
            IMAGES_FOLDER = config['TRAINING_IMAGES']
            if random.random() <= vperc:
                training = False
                IMAGES_FOLDER = config['VALIDATION_IMAGES']
            
            
            if lookingForEmotion:
                # Looking for Emotions
                emoInfo = readCkEmoFile(config['EMOLIST'], dataFile, subject, shot)
                if not emoInfo in config["CLSLIST"]:
                    print "No Emotion found for subject: {0} shot {1} in file: {2}".format(subject, shot, dataFile)
                    continue
                else:
                    # Last picture is the final emotion (most intense), first picture is neutral
                    to_copy = [(pics[-1], emoInfo), (pics[0], config['EMOLIST'][0])]
                    for pic, emo in to_copy:
                        print "INFO: Image '{}' has been marked as Emotion: {}".format(pic, emo)
                        orig = join(imgFolder, join(subject, join(shot, pic)))
                        
                        if training:
                            validationDataPath = join(dsFolder, join(config['VALIDATION_DATA'], join(emo, pic)))
                            writeValidationData(validationDataPath, emo.split(), False)                            
                            
                        dest = join(dsFolder, join(IMAGES_FOLDER, join(emo, pic)))
                        copyImageFile(orig, dest)
                
            else:
                # Looking for AU (will read in list of [AU, AU intensity]
                facsInfo = readFACSFile(dataFile)
                if (facsInfo == None):
                    print "No information found for subject: {0} shot {1} in file: {2}".format(subject, shot, dataFile)
                    continue
                else:
                    # Build Map of information
                    facsMap = {}
                    for facs in facsInfo:
                        facsMap[ facs[0] ] = facs[1]
                    
                    facsList = []
                    for facs in facsInfo:
                        facsList.append( facs[0] )
                    
                    if training:
                        for cls in config["SEARCH_LIST"]:
                            auFolder = "AU{}".format(cls)   # Occurrences where this AU does feature (default)
                            # Check for Occurrences where this AU does NOT feature 
                            if cls not in facsList:
                                auFolder = "NotAU{}".format(cls)
                            
                            IMAGES_FOLDER = config['TRAINING_IMAGES']
                            orig = join(imgFolder, join(subject, join(shot, pics[-1])))
                            dest = join(dsFolder, join(IMAGES_FOLDER, join(auFolder, pics[-1])))
                            copyImageFile(orig, dest)
                    else:
                        # Copy Validation Image
                        orig = join(imgFolder, join(subject, join(shot, pics[-1])))
                        dest = join(dsFolder, join(IMAGES_FOLDER, pics[-1]))
                        copyImageFile(orig, dest)

                        # Copy Validation Data
                        validationDataPath = join(dsFolder, join(config['VALIDATION_DATA'], pics[-1]))
                        writeValidationData(validationDataPath, facsList, True)

# ----------------------------------- FERA2015 Specific Information
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

def copyFile(sourceFile, subject, shot, auFolder, dsFolder, config, copyTo, auData):
    try:
        imagesFolder = config['TRAINING_IMAGES']
        if copyTo == "valid":
            imagesFolder = config['VALIDATION_IMAGES']
        
        # Randomly copy things for training
        fileName = "{}_{}_{}".format(subject, shot, os.path.basename(sourceFile))
        destPath = join(dsFolder, join(imagesFolder, join(auFolder, fileName)))
        
        if copyTo == "valid":
            validationDataPath = join(dsFolder, join(config['VALIDATION_DATA'], join(auFolder, fileName)))
            writeValidationData(validationDataPath, auData, True)
        
#         print "Copying: {}   ->   To: {}".format(sourceFile, destPath)     
        shutil.copy(sourceFile, destPath)
    except IOError as err:
        if not isfile(sourceFile):
            print "ERR: cannot copy image {0} > FILE DOES NOT EXIST".format(sourceFile)
        else:
            print "ERR: cannot copy image {0} to dataset {1} Reason: {2}".format(sourceFile, destPath, err.strerror)

def findMaxDigits(searchPath):
    fileName = locateFirstFile("*.jpg", searchPath)
    if (fileName == None):
        return 0
    else:
        return len( fileName )
    
def extractImageLimits(config, auList, isTraining):
    limit = -1
    auLimits = {}
    
    try:
        msg = "Training"
        if (isTraining):
            limit = config["RECOG_TRAIN_LIMIT"]
    
            for au in auList:
                auLimits["AU{}".format(au)] = int(limit)
                auLimits["NotAU{}".format(au)] = int(limit)
        else:
            msg = "Validation"
            limit = config["RECOG_VALIDATE_LIMIT"]
            auCountValidation = 0
            for au in auList:
                auCountValidation += int(limit)
    
            auLimits["valid"] = auCountValidation

        print "Limiting images for {} per AU: {}".format(msg, limit)    
    except:
        pass

    return auLimits 
    
def datasetFillFERA2015(dsFolder, feraImageFolder, auCodingFolder, config, vperc=0.3, vseed=0):
    print "Looking for the following AU: {0}".format( config["SEARCH_LIST"] )
    
    # Configuration Details
    # These are the AU you are looking for
#     auList = [int(x) for x in config["SEARCH_LIST"].split(",")]
    auList = config["SEARCH_LIST"]
    
    limits = {}
    limits["train"] = extractImageLimits(config, auList, True)
    limits["valid"] = extractImageLimits(config, auList, False)["valid"]
    
    print "Limits for training: {}".format(limits["train"])
    print "Limits for validation: {}".format(limits["valid"])
    
    #Read in FACS info [] in the format (path, fileName)
    processCount = 0
    for (path, fileName) in locateFile("*.csv", auCodingFolder):
        processCount += 1
    
    count = 1
    # process all AuCoding into a single dataset
    for (path, fileName) in locateFile("*.csv", auCodingFolder):
        info = fileName.replace(".csv", "").split("_")
        subject = info[0]
        shot = info[1]
        imageSearchPath = join(feraImageFolder, subject, shot)
        
        print "[%3d /%3d] Processing Subject: %s Set: %s"%(count, processCount, subject, shot)
        
        # Read in FACS Info File
        facsAuInfo = readFERA2015AUCoding(os.path.join(path, fileName))
        
        # need to find smallest + largest file (for padding mystery)
        # since some files are label 312.jpg and others 0312.jpg
        maxLength = findMaxDigits(imageSearchPath)
        
        for auDetails in facsAuInfo:
            
            # Check that one of the AU is at least present or not present (just not unknown)
            auPresent = [au for au in auList if au in auDetails.presentAU]
            auNotPresent = [au for au in auList if au in auDetails.notPresentAU]
            
            if len(auPresent) > 0 or len(auNotPresent) > 0:
                imageFile = "{}.jpg".format(auDetails.imageFileRef).rjust(maxLength, "0")
                image2Copy = join(imageSearchPath, locateFirstFile(imageFile,  imageSearchPath))
                
                # Next Image goes to...
                if (random.random() <= vperc) and (limits["valid"] > 0):
                    # Copy image into root of Validation /images folder
                    picFileDest = "{}_{}_{}".format(subject, shot, os.path.basename(image2Copy))
                    dest = join(dsFolder, join(config['VALIDATION_IMAGES'], picFileDest))
                    copyImageFile(picFileDest, dest)
                    
                    # Copy AU information for later validation 
                    validationDataPath = join(dsFolder, join(config['VALIDATION_DATA'], picFileDest))
                    writeValidationData(validationDataPath, auDetails.presentAU, True)
                    limits["valid"] = limits["valid"] - 1
                else:
                    checkAuSetLimits = False
                    for au in auList:
                        if au in auDetails.notPresentAU:
                            # First find images which are NOT the AU you are looking for 
                            currentAUCount = limits["train"]["NotAU{}".format(au)] 
                            if (currentAUCount != 0):
                                copyFile(image2Copy, subject, shot, "NotAU{}".format(au), dsFolder, config, "train", auDetails.presentAU)
                                currentAUCount = currentAUCount - 1
                                limits["train"]["NotAU{}".format(au)] = currentAUCount
                                if currentAUCount == 0:
                                    checkAuSetLimits = True
                            
                        elif au in auDetails.presentAU:
                            # Next find images which are the AU you are looking for
                            currentAUCount = limits["train"]["AU{}".format(au)] 
                            if (currentAUCount != 0):
                                copyFile(image2Copy, subject, shot, "AU{}".format(au), dsFolder, config, "train", auDetails.presentAU)
                                currentAUCount = currentAUCount - 1
                                limits["train"]["AU{}".format(au)] = currentAUCount
                                if currentAUCount == 0:
                                    checkAuSetLimits = True
                    
                    # Check if search limit for AU reached, then remove
                    if (checkAuSetLimits):
                        removeAu = []
                        for au in auList:
                            if (limits["train"]["AU{}".format(au)] == 0) and (limits["valid"]["AU{}".format(au)] == 0) and (limits["train"]["NotAU{}".format(au)] == 0) and (limits["valid"]["NotAU{}".format(au)] == 0):
                                removeAu.append(au)
                        for au in removeAu:
                            auList.remove(au);
                            print "No Longer looking for .... AU: {}".format(au)
                    
                    if (len(auList) == 0):
                        print "Finished..."
                        return
        count += 1

# ----------------------------------- Entry Point
def datasetFillImages(dsFolder,imgFolder, lblFolder, config, vperc=0.3, vseed=0):
    if (config["RECOG_DATABASE"].upper() == "CK"):
        dataset_fillCohnKanade(dsFolder, imgFolder, lblFolder, config, vperc, vseed)
    elif (config["RECOG_DATABASE"].upper() == "BP4D"):
        datasetFillFERA2015(dsFolder, imgFolder, lblFolder, config, vperc, vseed)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cfg", default="dataset.cfg", help="Dataset config file name")
    parser.add_argument("--validation-perc", dest='vperc', type=float, default=0.3, help="Validation set percentage (0-1.0)")
    parser.add_argument("--validation-seed", dest='vseed', type=int, default=0, help="Seed used to decide when a image belong to training or validation set")
    parser.add_argument("dsFolder", help="Dataset Base folder")
    parser.add_argument("imgFolder", help="Image database folder")
    parser.add_argument("lblFolder", help="Label folder")
    args = parser.parse_args()
    try:
        if args.vperc < 0.0 or args.vperc > 1.0:
            raise Exception("validation percentage must be in range 0-1 (%f)" % args.vperc)
        random.seed(args.vseed)
        config = {}
        config = dcp.parse_ini_config(args.cfg)
        datasetFillImages(args.dsFolder, args.imgFolder, args.lblFolder, config, vperc=args.vperc, vseed=args.vseed)
    except Exception as e:
        print "ERR: something wrong (%s)" % str(e)
        sys.exit(1)
