'''
Created on Jan 1, 2016

@author: John Eatwell
'''

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


def chunk(xs, percSplit):
    ys = list(xs)
    random.shuffle(ys)
    random.shuffle(ys)
    random.shuffle(ys)
    groupings = int(len(ys) * percSplit / 100.0 )
    chunks = [ys[n:n+groupings] for n in range(0, len(ys), groupings)]
    return chunks    
            
def createImageCSvFile(imgFolder, labelFolder, maxNeutral, maxEmotions, outputFile, imageSplitPercentage):
#     for subdir, dirs, files in os.walk(imgFolder):
#         for file in files:
# #             print os.path.join(subdir, file)
#             print dirs

    imageList = []
    
    subjects = [ x for x in os.listdir(imgFolder) if isdir(join(imgFolder, x)) ]
#     subjects.sort()
    
    for subject in subjects:
        labelFolders = [x for x in os.listdir(join(labelFolder, subject)) if isdir(join(labelFolder, join(subject, x)))]
        imageFolders = [x for x in os.listdir(join(imgFolder, subject)) if isdir(join(labelFolder, join(subject, x)))]
        shots = [x for x in imageFolders if x in labelFolders]
#         shots.sort()
        
        for shot in shots:
            images = [x for x in os.listdir(join(imgFolder, join(subject, shot))) if isfile(join(imgFolder, join(subject, join(shot, x))))]
            images.sort()
            
            neutralCount = int(len(images) * 0.1)
            if neutralCount < 1:
                neutralCount = 1
            elif neutralCount > maxNeutral: 
                neutralCount = maxNeutral
            
            emotionCount = int(len(images) * 0.3)
            if emotionCount < 1:
                emotionCount = 1
            elif emotionCount > maxEmotions: 
                emotionCount = maxEmotions
            
            imageFiles = images[:neutralCount] + images[-emotionCount:]
            for image in imageFiles:
                if image.endswith("png"):
                    imageList.append( "{}/{}/{}".format(subject, shot, image) )
    
    # Split file into training and testing
    trainSplit = chunk(imageList, imageSplitPercentage)
    writeOutput(outputFile, trainSplit[0], trainSplit[1])
    
    print "Records written to {}: {} using a {}% split".format(outputFile, len(imageList), imageSplitPercentage)
    
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
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("imgFolder", help="Image database folder")
    parser.add_argument("labelFolder", help="label database folder")
    parser.add_argument("outputFile", help="Output CSV File")
    args = parser.parse_args()
    try:
        createImageCSvFile(args.imgFolder, args.labelFolder, 2, 5, args.outputFile, 80)
    except Exception as e:
        print "ERR: something wrong (%s)" % str(e)
        sys.exit(1)