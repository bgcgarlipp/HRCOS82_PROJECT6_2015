#!/usr/bin/env python2
'''
    File name:      auUtils.py
    Author:         John Eatwell (35264926)
    Date created:   10/09/2015
    Python Version: 2.7
	Details:        Utilities file for file operations
'''
import os
import fnmatch

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
    
def locateFile(filePattern, curFolder=os.curdir):
    '''
        Locate all files matching supplied filename pattern in and below supplied rootcurFolderfolder.
    '''
    for (path, dir, files) in sorted(os.walk(os.path.abspath(curFolder))):
        for fileName in sorted(fnmatch.filter(files, filePattern)):
            yield (path, fileName)
            
def locateFirstFile(filePattern, curFolder=os.curdir):
    '''
        Locate First file matching supplied filename pattern in and below supplied curFolder.
    '''
    
    for (path, dir, files) in os.walk(os.path.abspath(curFolder)):
        for fileName in fnmatch.filter(files, filePattern):
            return fileName
            
            
def isSubSet(arr, container):
    '''
        Find if arr is fully contained in container
    '''
    for el in arr:
        if not el in container:
            return False 
    return True

if __name__ == '__main__':
    fileName = locateFirstFile("*.jpg", "/home/bluedaemon/Projects/fer/autime/prj/databases/BP4D/images/M010/T4")
    print fileName
    