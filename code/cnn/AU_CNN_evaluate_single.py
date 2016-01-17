"""
    Python modules to import
"""
import os
import sys
import numpy as np
from pandas.io.parsers import read_csv
from pandas import DataFrame
from sklearn.utils import shuffle
import matplotlib.pyplot as pyplot
import lasagne
from lasagne import layers,nonlinearities
from lasagne.updates import nesterov_momentum
from nolearn.lasagne import NeuralNet,BatchIterator
import theano.tensor as T
import cPickle as pickle
from performVerification import ConfusionMatrix
import cv2
from PIL import Image
import matplotlib.pyplot as pyplot
import csv
from data_pre_processing.face_detect_single import FaceCrop
import time
"""
    Initialze face cropper
"""
THRESHOLD = 0.5
cropper = FaceCrop()
PIX = 48
"""
    pickled object location
"""
pickled_file_location = 'cnn_trained/BP4D_48_48_train..pickle'
"""
    predefined AU list to compare
"""
AU_list_initial = [1 ,2, 4, 6, 7, 10, 12, 14 ,15, 17, 23]


"""
    Thresehold to decide if it clasified correctly
"""

"""
    CNN objects
"""
cnn_objetc = None

"""
    Function to load csv files into pandas frame
"""
def load(filename):
    img = cropper.getCrop(filename)
    if img is not None:
        """
            use opencv to resize and write images
        """
        resized = cv2.resize(img,(PIX,PIX))
    else:
        print "No face could be detected"
        sys.exit()
    df = DataFrame(columns=('filename', 'Image'))
    output =  ' '.join(' '.join(str(cell) for cell in row) for row in resized)
    df.loc[0] = [filename,output]
    # The Image column has pixel values separated by space; convert
    # the values to numpy arrays:
    df['Image'] = df['Image'].apply(lambda im: np.fromstring(im, sep=' '))
    X = np.vstack(df['Image'].values) / 255.  # scale pixel values to [0, 1]
    X = X.astype(np.float32)
    del df['filename']
    y = None
    return X, y

"""
    refactor data to 2d array
"""
def load2d(filename):
    X, y = load(filename)
    X = X.reshape(-1, 1, PIX, PIX)
    return X, y


cnn_object = pickle.load(open(pickled_file_location,'rb'))
print "loading Data"
if sys.argv[1] is not None:
    print "File to find", sys.argv[1]
    data = load2d(sys.argv[1])[0]  # load 2-d data
    print "Training"
    """
        load test data
    """
    y_pred = cnn_object.predict(data)

    
    for i,results in enumerate(y_pred):
        output_sting = ""
        for i2,result in enumerate(results):
            AU = AU_list_initial[i2]
            
            if result >= THRESHOLD:
                output_sting+= "AU"+str(AU)+":"+"1,"
            elif result < THRESHOLD :
                output_sting+= "AU"+str(AU)+":"+"0,"
        f = open("output.txt","w")
        f.write(output_sting)
        f.close()
        print output_sting
else:
    print "please pcovide a image"

  
