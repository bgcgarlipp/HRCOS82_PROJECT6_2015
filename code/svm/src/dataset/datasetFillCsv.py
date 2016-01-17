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
from reportlab.lib.units import pica

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
# --------------------------------------------------------------------------------------------------------------------

def dataset_fillCohnKanade(dsFolder, imgFolder, labelFolder, config, csvFileName, createReferenceFile):
    # Check if reading emotions or AU    
    lookingForEmotion = False
    if (config["RECOG_TYPE"].upper() == "EMOTION"):
        lookingForEmotion = True
    
    # Process CSV File (each line reads: IMAGE, training/test  
    csvFile = open(csvFileName, "r")
    for line in csvFile:
        if (len(line) > 1):
            data = line[:-1].split(",")
            isTesting = data[1].lower().startswith("test")
            subjectInfo = data[0].split("/")
            subject = subjectInfo[0]
            shot = subjectInfo[1]
            picFile = subjectInfo[2]
            picFilePath = join(imgFolder, join(subject, join(shot, picFile)))
            labelFolderPath = join(labelFolder, join(subject, shot))
            
            IMAGES_FOLDER = config['TRAINING_IMAGES']
            if isTesting:
                IMAGES_FOLDER = config['VALIDATION_IMAGES']
            
            # read FACS / emotion data
            if isdir(labelFolderPath) and isfile(picFilePath):
                labels = [x for x in os.listdir(labelFolderPath) if isdir(labelFolderPath) and isfile(join(labelFolder, join(subject, join(shot, x)))) ]
                for fileName in labels:
                    dataFile = join(labelFolder, join(subject, join(shot, fileName)))
                    if lookingForEmotion:
                        # Looking for Emotions
                        emoInfo = readCkEmoFile(config['EMOLIST'], dataFile, subject, shot)
                        if not emoInfo in config["CLSLIST"]:
                            print "No Emotion found for subject: {0} shot {1} in file: {2}".format(subject, shot, dataFile)
                            continue
                        else:
                            # first picture(s) are neutral
                            num = int(picFile[:-4][-3:])
                            if num <= 5:
                                emoInfo = config['EMOLIST'][0]
                            
                            print "INFO: Image '{}' has been marked as Emotion: {}".format(picFile, emoInfo)
                            
                            # Copy Images
                            orig = join(imgFolder, join(subject, join(shot, picFile)))
                            dest = ""
                            if isTesting:
                                validationDataPath = join(dsFolder, join(config['VALIDATION_DATA'], picFile))
                                writeValidationData(validationDataPath, emoInfo.split(), False)
                                dest = join(dsFolder, join(IMAGES_FOLDER, picFile))
                            else:
                                if createReferenceFile:
                                    dest = join(dsFolder, join(IMAGES_FOLDER, join(emoInfo, "images.txt"))) 
                                else:
                                    dest = join(dsFolder, join(IMAGES_FOLDER, join(emoInfo, picFile)))
                                    
                            
                            if (not isTesting) and createReferenceFile:
                                writeImageReference(dest, picFilePath)
                            else:
                                copyImageFile(orig, dest)
                                
                    else:
                        # Looking for AU
                        facsInfo = readFACSFile(dataFile)
                        if (facsInfo == None):
                            print "No information found for subject: {0} shot {1} in file: {2}".format(subject, shot, dataFile)
                            continue
                        else:
                            facsList = []
                            for facs in facsInfo:
                                facsList.append( facs[0] )
                                
                            if isTesting:
                                validationDataPath = join(dsFolder, join(config['VALIDATION_DATA'], picFile))
                                writeValidationData(validationDataPath, facsList, True)
                                dest = join(dsFolder, join(IMAGES_FOLDER, picFile))
                                copyImageFile(picFilePath, dest)
                            else:
                                for cls in config["SEARCH_LIST"]:
                                    auFolder = "AU{}".format(cls)   # Occurrences where this AU does feature (default)
                                    
                                    # Check for Occurrences where this AU does NOT feature 
                                    if cls not in facsList:
                                        auFolder = "NotAU{}".format(cls)
                                    
                                    if createReferenceFile:
                                        dest = join(dsFolder, join(IMAGES_FOLDER, join(auFolder, "images.txt")))
                                    else:
                                        dest = join(dsFolder, join(IMAGES_FOLDER, join(auFolder, picFile)))
                                    
                                    if (not isTesting) and createReferenceFile:
                                        writeImageReference(dest, picFilePath)
                                    else:
                                        copyImageFile(picFilePath, dest)
            else:
                if not isdir( labelFolderPath ):
                    print "Problem resolving directory: {}".format( dir )
                else:
                    print "Problem resolving image file: {}".format( picFilePath )

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

def writeImageReference(path, imageReference):
    try:
        with open(path, 'a+') as f:
            f.write("{}\n".format(imageReference))
    except IOError as e:
        print "I/O error({0}): writing file {1}".format(e.strerror, path)
        
def datasetFillFERA2015(dsFolder, imgFolder, labelFolder, config, csvFileName, createReferenceFile):
    print "Processing FERA2015 CSV File"
    # Process CSV File (each line reads: IMAGE, training/test
    auList = config["SEARCH_LIST"]
    lastLabelFolderPath = ""
    facsAuInfo = []
    imageProcessCount = 0
    
    csvFile = open(csvFileName, "r")
    for line in csvFile:
        if (len(line) > 1):
            data = line[:-1].split(",")
            isTesting = data[1].lower().startswith("test")
            subjectInfo = data[0].split("/")
            subject = subjectInfo[0]
            shot = subjectInfo[1]
            
            picFile = subjectInfo[2]
            picFilePath = join(imgFolder, join(subject, join(shot, picFile)))

            labelFile = "{}_{}.csv".format(subject, shot)
            labelFolderPath = join(labelFolder, labelFile)

            auIndex = "{}".format( int(picFile[:-4]) )

            IMAGES_FOLDER = config['TRAINING_IMAGES']
            if isTesting:
                IMAGES_FOLDER = config['VALIDATION_IMAGES']
            
            # read FACS / emotion data
            if isfile(labelFolderPath) and isfile(picFilePath):
                
                # Read in FACS Info File (Expensive so only done if necessary)
                if lastLabelFolderPath != labelFolderPath:
                    print "INFO: Processing Label: {} First Image: {} Last Image count processed: {}".format(labelFile, picFile, imageProcessCount)
                    facsAuInfo = readFERA2015AUCoding(labelFolderPath)
                    lastLabelFolderPath = labelFolderPath
                    imageProcessCount = 0

                for auDetails in facsAuInfo:
                    # first find the image you are looking for
                    if auDetails.imageFileRef == auIndex:
                        
                        # Picture files are too simplistic
                        picFileDest = "{}_{}_{}".format(subject, shot, picFile)
                        
                        if isTesting:
                            validationDataPath = join(dsFolder, join(config['VALIDATION_DATA'], picFileDest))
                            writeValidationData(validationDataPath, auDetails.presentAU, True)
                            
#                             if createReferenceFile:
#                                 dest = join(dsFolder, join(IMAGES_FOLDER, "images.txt"))
#                                 writeImageReference(dest, picFilePath)
#                             else:
                            dest = join(dsFolder, join(IMAGES_FOLDER, picFileDest))
                            copyImageFile(picFilePath, dest)
                        else:
                            for au in auList:
                                if au in auDetails.unknownAU:
                                    continue
                                else:
                                    auFolder = "AU{}".format(au)
                                    
                                    # Find images which are NOT the AU you are looking for
                                    if au in auDetails.notPresentAU:
                                        auFolder = "NotAU{}".format(au)
                                    
                                    if createReferenceFile:
                                        dest = join(dsFolder, join(IMAGES_FOLDER, join(auFolder, "images.txt")))
                                        writeImageReference(dest, picFilePath)
                                    else:
                                        dest = join(dsFolder, join(IMAGES_FOLDER, join(auFolder, picFileDest)))
                                        copyImageFile(picFilePath, dest)
                                    imageProcessCount += 1
                        break
            else:
                if not isfile( labelFolderPath ):
                    print "Problem resolving label file: {}".format( labelFolderPath )
                else:
                    print "Problem resolving image file: {}".format( picFilePath )

# ----------------------------------- Entry Point
def datasetFillImages(dsFolder, imgFolder, lblFolder, config, csvFileName, createReferenceFile):
    if (config["RECOG_DATABASE"].upper() == "CK"):
        dataset_fillCohnKanade(dsFolder, imgFolder, lblFolder, config, csvFileName, createReferenceFile)
    elif (config["RECOG_DATABASE"].upper() == "BP4D"):
        datasetFillFERA2015(dsFolder, imgFolder, lblFolder, config, csvFileName, createReferenceFile)

 
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cfg", default="dataset.cfg", help="Dataset config file name")
    parser.add_argument("--csv", help="CSV File containing configuration")
    parser.add_argument("dsFolder", help="Dataset Base folder")
    parser.add_argument("imgFolder", help="Image database folder")
    parser.add_argument("lblFolder", help="Label folder")
    parser.add_argument("--nomove", action="store_true", help="Do not move database files, rather create a file to reference")
    args = parser.parse_args()
    try:
        config = {}
        config = dcp.parse_ini_config(args.cfg)
        datasetFillImages(args.dsFolder, args.imgFolder, args.lblFolder, config, args.csv, args.nomove)
    except Exception as e:
        print "ERR: something wrong (%s)" % str(e)
        sys.exit(1)