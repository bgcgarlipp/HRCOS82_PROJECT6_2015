"""
    Python module imports
"""
import os
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as pyplot
import csv
from random import randint
from face_detect import FaceCrop
import time
"""
 Dictionary of datasets base image folders
"""
images_folder = {}
images_folder['BP4D']  =  '../../databases/BP4D/images'
images_folder['CK']  = '../../databases/cohn-kanade/images'
"""
    Desired Pixel data sets
""" 
IMAGE_PIX = [16,24,32,40,48,56,96]
"""
    Folder to see cropped images in, used for debugging
"""
CROPPEd_FOLDER = 'Cropped_Images'



"""
    Get start time
"""
t0 = time.time()
"""
    Initialze face cropper
"""
cropper = FaceCrop()
"""
    Loop trougheach dataset
"""
for name,dataset in  images_folder.items():
    """
    Progres counters
    """
    Total = 0.0
    Total_time = 0.0
    progres = 0.0
    filecount = 0
    added = 0
    notadded = 0
    """
        Counts the number of files, to show progress
    """
    for subdir, dirs, files in os.walk(dataset):
        Total += len(files)* len(IMAGE_PIX)
    print 'Total Files : ',Total
    print name
    """
        Loop trough each sub dataset to crop and resize
    """
    for subdir, dirs, files in os.walk(dataset):
        for file in files:
            filecount += 1
            file_still_needs_to_be_created = False
            for res in IMAGE_PIX:
                folders = subdir.split('/')
                if not os.path.exists(os.path.join('datasets',name+'_'+str(res)+'X'+str(res),folders[len(folders)-2],folders[len(folders)-1],file)):
                    
                    file_still_needs_to_be_created = True
                    break
            if not file_still_needs_to_be_created:
                added += 1 * len(IMAGE_PIX)
                #print "file exists, not recreating"
                continue
            img_filename =  os.path.join(subdir, file)
            """
                get croped image
            """
            img = cropper.getCrop(img_filename)
            if img is None:
                img = cropper.getCrop(img_filename)
            """
                Resize image for each resolution
            """
            for res in IMAGE_PIX:
                """
                    Make sure the foldres exists
                """
                if os.path.exists(os.path.join('datasets',name+'_'+str(res)+'X'+str(res))):
                    if os.path.exists(os.path.join('datasets',name+'_'+str(res)+'X'+str(res),folders[len(folders)-2])):
                        if os.path.exists(os.path.join('datasets',name+'_'+str(res)+'X'+str(res),folders[len(folders)-2],folders[len(folders)-1])):
                            pass
                        else:
                            os.mkdir(os.path.join('datasets',name+'_'+str(res)+'X'+str(res),folders[len(folders)-2],folders[len(folders)-1]))
    
                    else:
                        os.mkdir(os.path.join('datasets',name+'_'+str(res)+'X'+str(res),folders[len(folders)-2]))
                        if os.path.exists(os.path.join('datasets',name+'_'+str(res)+'X'+str(res),folders[len(folders)-2],folders[len(folders)-1])):
                            pass
                        else:
                            os.mkdir(os.path.join('datasets',name+'_'+str(res)+'X'+str(res),folders[len(folders)-2],folders[len(folders)-1]))
                else:
                    os.mkdir(os.path.join('datasets',name+'_'+str(res)+'X'+str(res)))
                    if os.path.exists(os.path.join('datasets',name+'_'+str(res)+'X'+str(res),folders[len(folders)-2])):
                        if os.path.exists(os.path.join('datasets',name+'_'+str(res)+'X'+str(res),folders[len(folders)-2],folders[len(folders)-1])):
                            pass
                        else:
                            os.mkdir(os.path.join('datasets',name+'_'+str(res)+'X'+str(res),folders[len(folders)-2],folders[len(folders)-1]))
    
                    else:
                        os.mkdir(os.path.join('datasets',name+'_'+str(res)+'X'+str(res),folders[len(folders)-2]))
                        if os.path.exists(os.path.join('datasets',name+'_'+str(res)+'X'+str(res),folders[len(folders)-2],folders[len(folders)-1])):
                            pass
                        else:
                            os.mkdir(os.path.join('datasets',name+'_'+str(res)+'X'+str(res),folders[len(folders)-2],folders[len(folders)-1]))
                """
                    Check if a face was found
                """
                if img is not None:
                    """
                        use opencv to resize and write images
                    """
                    resized = cv2.resize(img,(res,res))
                    cv2.imwrite(os.path.join('datasets',name+'_'+str(res)+'X'+str(res),folders[len(folders)-2],folders[len(folders)-1],file),resized)
                    added += 1
                else:
                    notadded +=1
            if filecount %100 == 0:
                tf = time.time()
                print ' Total Percentage Done: ' , filecount/Total *100,  " added ",added," not added ",notadded, "time ",tf-t0
                t0 = time.time()

   
