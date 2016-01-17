"""
=============================================================================
Author : Bernhardt Garlipp
Unisa Student : 47814136
Project: A comparitive study between CCN and SVM
Date : 2015-02-18 - 2016-01-17
=============================================================================

Description : This code instaniates the CNN object of the python Lasagne. The paramters used in this section for the CNN i derived from the paper 
FERA_2015_Deeplearning 

"""
"""
    Python modules to import
"""
import os
import theano
import numpy as np
from numpy import float32
from pandas.io.parsers import read_csv
from sklearn.utils import shuffle
import matplotlib.pyplot as pyplot
import lasagne
from lasagne import layers,nonlinearities
from lasagne.updates import nesterov_momentum
from nolearn.lasagne import NeuralNet,BatchIterator
import theano.tensor as T
import cPickle as pickle
from performVerification import ConfusionMatrix

class AdjustVariable(object):
    def __init__(self, name, start=0.03, stop=0.001):
        self.name = name
        self.start, self.stop = start, stop
        self.ls = None

    def __call__(self, nn, train_history):
        if self.ls is None:
            self.ls = np.linspace(self.start, self.stop, nn.max_epochs)

        epoch = train_history[-1]['epoch']
        new_value = float32(self.ls[epoch - 1])
        getattr(nn, self.name).set_value(new_value)
"""
    pickled object location
"""
pickled_location = 'cnn_trained'
"""
    location of input data csv
"""
datalocation = 'data'
"""
    predefined AU list to compare
"""
AU_list_initial = [1 ,2, 4, 6, 7, 10, 12, 14 ,15, 17, 23]
"""
   training sets
   filename : location 
"""
training_data = {}
"""
    populate training data
"""
print "Geting training sets"
for subdir, dirs, files in os.walk(datalocation):
    for file in files:
        if 'train' in file:
            training_data[file] = os.path.join(subdir,file)

"""
    Labels
"""
labels =[]
"""
    Statsitics on AU
"""
AU_stat= {}
for au in AU_list_initial:
    AU_stat[au] = {'correct':0,'incorrect':0,'total':0}
"""
    Thresehold to decide if it clasified correctly
"""
THRESHOLD =0.5
"""
    Input columns generated from AU_list_initial
"""
INPUT_COLUMNS = [str(x) for x  in AU_list_initial +['filename']]#['0','1','2','3','4','5','6','filename']
"""
    CNN objects
"""
cnn_objetcs = {}

"""
    Function to load csv files into pandas frame
"""
trainamount = None

"""
    epoche count
"""
epouch_count = [500]

def load(fname,cols=None,pixels=48):
    global labels
    df = read_csv(os.path.expanduser(fname))  # load pandas dataframe
    #print "number of entries", df.count
    # The Image column has pixel values separated by space; convert
    # the values to numpy arrays:
    df['Image'] = df['Image'].apply(lambda im: np.fromstring(im, sep=' '))
    df_temp = df
    labels = df_temp.values.tolist()
    if cols:  # get a subset of columns
        df = df[list(cols) + ['Image']]
    for index, row in df.iterrows():
        if row['Image'].size != pixels* pixels:
            print row
    # test to see ssize of image should equal widthx height
    #print [x.size for x in df['Image'].values]
    df = df.dropna()  # drop all rows that have missing values in them
    #df.iloc[np.random.permutation(len(df))]
    if trainamount is not None:
        df = df.head(trainamount)
    #print "new number of entries", df.count
    #df = df[df.Image.size !=pixels*pixels ]
    X = np.vstack(df['Image'].values) / 255.  # scale pixel values to [0, 1]
    X = X.astype(np.float32)
    del df['filename']
    y = df[df.columns[:-1]].values
    #X, y = shuffle(X, y, random_state=42)  # shuffle train data
    y = y.astype(np.float32)
    return X, y

"""
    refactor data to 2d array
"""
def load2d(fname=None,cols=None,pixels=48):
    X, y = load(fname=fname,cols=cols,pixels=pixels)
    X = X.reshape(-1, 1, pixels, pixels)
    return X, y

for file,location in training_data.items():
    print "Starting with : " + file
    pixels = int(file.split('_')[1])
    for epoche in epouch_count:
        """ 
            CNN definition, Improved version from example, gives good results
#         """
#         cnn_objetcs[file]= NeuralNet(
#             layers=[
#                 ('input', layers.InputLayer),
#                 ('conv1', layers.Conv2DLayer),
#                 ('pool1', layers.MaxPool2DLayer),
#                 ('dropout1', layers.DropoutLayer),  # !
#                 ('conv2', layers.Conv2DLayer),
#                 ('pool2', layers.MaxPool2DLayer),
#                 ('dropout2', layers.DropoutLayer),  # !
#                 ('conv3', layers.Conv2DLayer),
#                 ('pool3', layers.MaxPool2DLayer),
#                 ('dropout3', layers.DropoutLayer),  # !
#                 ('hidden4', layers.DenseLayer),
#                 ('dropout4', layers.DropoutLayer),  # !
#                 ('hidden5', layers.DenseLayer),
#                 ('output', layers.DenseLayer),
#                 ],
#             input_shape=(None, 1, pixels, pixels),
#             conv1_num_filters=32, conv1_filter_size=(3, 3), pool1_pool_size=(2, 2),
#             dropout1_p=0.1,  # !
#             conv2_num_filters=64, conv2_filter_size=(2, 2), pool2_pool_size=(2, 2),
#             dropout2_p=0.2,  # !
#             conv3_num_filters=128, conv3_filter_size=(2, 2), pool3_pool_size=(2, 2),
#             dropout3_p=0.3,  # !
#             hidden4_num_units=500,
#             dropout4_p=0.5,  # !
#             hidden5_num_units=500,
#             output_num_units=11, output_nonlinearity=nonlinearities.sigmoid,
#            
#             update_learning_rate=theano.shared(float32(0.03)),
#             update_momentum=theano.shared(float32(0.9)),
#            
#             regression=True,
#             #batch_iterator_train=FlipBatchIterator(batch_size=128),
#             on_epoch_finished=[
#                 AdjustVariable('update_learning_rate', start=0.03, stop=0.0001),
#                 AdjustVariable('update_momentum', start=0.9, stop=0.999),
#                 ],
#             max_epochs=epoche,
#             verbose=1,
#         )
        """
        Fera 2015 paper parameters
        """
        cnn_objetcs[file] = NeuralNet(
            layers=[
                ('input', layers.InputLayer),
                ('conv1', layers.Conv2DLayer),
                ('pool1', layers.MaxPool2DLayer),
                ('conv2', layers.Conv2DLayer),
                #('pool2', layers.MaxPool2DLayer),
                ('conv3', layers.Conv2DLayer),
               # ('pool3', layers.MaxPool2DLayer),
                ('hidden4', layers.DenseLayer),
                ('dropout4',layers.DropoutLayer),
                ('output', layers.DenseLayer),
                ],
            # input layer
            input_shape=(None, 1, pixels, pixels),
            conv1_num_filters=64, conv1_filter_size=(5, 5),conv1_stride = 1, pool1_pool_size=(3, 3),pool1_stride=2,
            conv2_num_filters=64, conv2_filter_size=(5, 5), #pool2_pool_size=(2, 2),
            conv3_num_filters=128, conv3_filter_size=(4, 4), #pool3_pool_size=(2, 2),
            hidden4_num_units=3072, dropout4_p=0.2,
   
            output_num_units=len(INPUT_COLUMNS)-1, 
            verbose=1,
            output_nonlinearity=nonlinearities.sigmoid,    
            update=nesterov_momentum,
            update_learning_rate=0.01,
            update_momentum=0.975,
            max_epochs=epoche,
            # #Here are the important parameters for multi labels
            regression=True,
            objective_loss_function=lasagne.objectives.binary_crossentropy,
             
            )
        """
            Basic CNN structure to get started with. Avarge results, but runs quikcly
        """
#         cnn_objetcs[file] = NeuralNet(
#             layers=[
#                 ('input', layers.InputLayer),
#                 ('conv1', layers.Conv2DLayer),
#                 ('pool1', layers.MaxPool2DLayer),
#                 ('conv2', layers.Conv2DLayer),
#                 ('pool2', layers.MaxPool2DLayer),
#                 ('conv3', layers.Conv2DLayer),
#                 ('pool3', layers.MaxPool2DLayer),
#                 ('hidden4', layers.DenseLayer),
#                 ('dropout4',layers.DropoutLayer),
#                 ('hidden5', layers.DenseLayer),
#                 ('dropout5',layers.DropoutLayer),
#                 ('output', layers.DenseLayer),
#                 ],
#             # input layer
#             input_shape=(None, 1, pixels, pixels),
#             conv1_num_filters=32, conv1_filter_size=(3, 3), pool1_pool_size=(2, 2),
#             conv2_num_filters=64, conv2_filter_size=(3, 3), pool2_pool_size=(2, 2),
#             conv3_num_filters=128, conv3_filter_size=(3, 3), pool3_pool_size=(2, 2),
#             hidden4_num_units=200, #dropout4_p=0.2,
#             hidden5_num_units=200,#dropout5_p=0.2,
#             output_num_units=len(INPUT_COLUMNS)-1, 
#             verbose=1,
#             output_nonlinearity=nonlinearities.sigmoid,    
#             update=nesterov_momentum,
#             update_learning_rate=0.01,
#             update_momentum=0.975,
#             max_epochs=40,
#             # #Here are the important parameters for multi labels
#             regression=True,
#             objective_loss_function=lasagne.objectives.binary_crossentropy,
#         )
        
        print "loading Data"
        X, y = load2d(fname=location,cols=INPUT_COLUMNS,pixels=pixels)  # load 2-d data
        print "Training"
        cnn_objetcs[file].fit(X, y)
        #Training for 1000 epochs will take a while.  We'll pickle the
        # trained model so that we can load it back later:
        print "Saving CNN"
        with open(os.path.join(pickled_location,file.replace("csv","")+'.pickle'+"_"+str(epoche)), 'wb') as f:
            pickle.dump(cnn_objetcs[file], f, -1)
      
