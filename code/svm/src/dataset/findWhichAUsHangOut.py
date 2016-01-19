#!/usr/bin/env python2

'''
    File name:      findWhichAUsHangOut.py
    Update Author:  John Eatwell (35264926)
    Date created:   10/09/2015
    Python Version: 2.7
	Details:        This was a fun side project which we did to see groupings of AU, when we thought that we could use AU to link to Emotions
'''

import os
import sys
import sets
import operator

from os.path import join
from os.path import isfile
from os.path import isdir

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
    
def findAUWhichAoocTogether(ckEmoFolder, resultsFileAUSort, resultsFileCountSort, resultsFileNoConflict):
    ''' 
        Read in all FACS AU and group them to answer 
        the questions: 
        1) Which AU are found together?
        2) And in what quantities
        
        To do so create

             dict(AU_primary, dict(AU_simbling, count))
             
        where the inner AU_sibling is found together with AU_primary, count times
    '''
    auSiblings = {}         #dict<AU, dict<AU, Count>>
    auCount = {}            #dict<AU, Count>
    allAU = set()
        
    subjects = [ x for x in os.listdir(ckEmoFolder) if isdir(join(ckEmoFolder, x)) ]
    for subject in subjects:
        labelFolders = [x for x in os.listdir(join(ckEmoFolder, subject)) if isdir(join(ckEmoFolder, join(subject, x)))]
        for shot in labelFolders:
            labels = [x for x in os.listdir(join(ckEmoFolder, join(subject, shot))) if isfile(join(ckEmoFolder, join(subject, join(shot, x)))) ]
            facsFile = join(ckEmoFolder, join(subject, join(shot, labels[0])))
            facsInfo = readFACSFile(facsFile)
            
            # Which AU are present in
            auSet = set()
            for au in facsInfo:
                auSet.add(au[0])
                allAU.add(au[0])
                if au[0] in auCount:
                    auCount[au[0]] = auCount[au[0]] + 1
                else:
                    auCount[au[0]] = 1
                
            for au in auSet:
                if not au in auSiblings:
                    auSiblings[au] = dict()
                
                # each dictionary inside the primary contains a count 
                # of the occurrences with the primary au
                others = set(auSet)
                others.remove(au)
                for oau in others:
                    if oau in auSiblings[au]:
                        count = auSiblings[au][oau] + 1
                        auSiblings[au][oau] = count
                    else:
                        auSiblings[au][oau] = 1
            
    # write results to file
    fAuSorted = open(resultsFileAUSort, "w")
    fCountSorted = open(resultsFileCountSort, "w")
    fNoConflict = open(resultsFileNoConflict, "w")
    
    
    for au in auSiblings:
        header = " AU [ {} ], instances [ {} ], siblings:{}".format(au, auCount[au], os.linesep)
        header = "{}{}{}".format(header, ("-" * len(header)), os.linesep)
        fAuSorted.write(header)
        fCountSorted.write(header)
        
        header = " AU [ {} ], instances [ {} ], No Conflict AUs:{}".format(au, auCount[au], os.linesep)
        header = "{}{}{}".format(header, ("-" * len(header)), os.linesep)
        fNoConflict.write(header)
        
        # Holsd array of non conflicting AU
        noConflict = set(allAU)
        noConflict.remove(au)
        
        # Sorted by AU
        for aus in auSiblings[au]:
            str = "  au: %2d   count: %d%s" %(aus, auSiblings[au][aus], os.linesep)
            fAuSorted.write(str)
            noConflict.remove(aus)
        
        # Sorted by Count
        for aus in sorted(auSiblings[au].items(), key=operator.itemgetter(1), reverse=True):
            str = "  count: %3d    au: %d%s" %(aus[1], aus[0], os.linesep)
            fCountSorted.write(str)
        
        # Write no Conflict    
        line = ""
        for auX in noConflict:
            if len(line) > 0:
                line = "{}, ".format(line)
            line = "{}{}".format(line, auX)
        fNoConflict.write(line + os.linesep)
        
        fAuSorted.write(os.linesep)
        fCountSorted.write(os.linesep)
        fNoConflict.write(os.linesep)
        
if __name__ == "__main__":
    facsFolderRoot = "../../databases/aucoding"
    resultsFileAUSort = "results_AU_sorted.txt"
    resultsFileCountSort = "results_count_sorted.txt"
    resultsFileNoConflict = "results_no_conflict.txt"
    
    print "Processing: {}".format(facsFolderRoot)
    findAUWhichAoocTogether( facsFolderRoot, resultsFileAUSort, resultsFileCountSort, resultsFileNoConflict)
    print "see '{}' and '{}' for results".format( resultsFileAUSort,  resultsFileCountSort)
