"""
    Python modules to import
"""
import os
import numpy as np
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
test_data = {}
"""
    populate training data
"""
print "Geting training sets"
for subdir, dirs, files in os.walk(datalocation):
    for file in files:
        if 'test' in file:
            test_data[file] = os.path.join(subdir,file)
"""
    Pickled files
"""
cnn_pickled = {}
print "Geting pickled sets"
for subdir, dirs, files in os.walk(pickled_location):
    for file in files:
        cnn_pickled[file] = os.path.join(subdir,file)
print cnn_pickled
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
THRESHOLD =0.50
"""
    Input columns generated from AU_list_initial
"""
INPUT_COLUMNS = [str(x) for x  in AU_list_initial +['filename']]#['0','1','2','3','4','5','6','filename']
"""
    CNN objects
"""
cnn_objetcs = {}

"""
    results folder
"""
results_folder = 'results'
"""
    pickled objects to loop trough
"""
pickled_files = {}
"""
    Function to load csv files into pandas frame
"""
def load(fname,cols=None):
    global labels
    df = read_csv(os.path.expanduser(fname))  # load pandas dataframe
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
    X = np.vstack(df['Image'].values) / 255.  # scale pixel values to [0, 1]
    X = X.astype(np.float32)
    del df['filename']
    y = df[df.columns[:-1]].values
    X, y = shuffle(X, y, random_state=42)  # shuffle train data
    y = None
    return X, y

"""
    refactor data to 2d array
"""
def load2d(fname=None,cols=None,pixels=48):
    X, y = load(fname=fname,cols=cols)
    X = X.reshape(-1, 1, pixels, pixels)
    return X, y

for file,location in test_data.items():
    if 'BP4D' in file:
        INDEX_ADJUST = 0
    elif 'CK' in file:
        INDEX_ADJUST = 0

    pixels = int(file.split('_')[1])
    """
        load trained CNN
    """
    pickle_file  = None
    output_file = None
    pickled_files = {}
    #print file
    for filename,pickled_file in cnn_pickled.items():
        fileinfo = filename.split('.')
        output_file = filename
        #print fileinfo
        if fileinfo[0].replace('_train','_test') in file:
            pickle_file = open(pickled_file,'rb')
            pickled_files[output_file] = pickled_file
    if pickled_files == {}:
        continue
    for output_file,pfile in pickled_files.items():
        pickle_file = open(pfile,'rb')
        print "Starting with : " + output_file ,"Using :"+file
        cnn_objetcs[file] = pickle.load(pickle_file)
        print "loading Data"
        data = load2d(fname=location,cols=INPUT_COLUMNS,pixels=pixels)[0]  # load 2-d data
        print "Evaluating"
        """
            load test data
        """
        print "Data length :" + str(len(data))
        y_pred = cnn_objetcs[file].predict(data)
         
        TPCount = 0  # predicted == actual 
        FPCount = 0  # predicted != actual
        TNCount = 0  #
        FNCount = 0  # predicted == unknown
        """
            Sensitivity
            TPR = TPCount/(TPCount + FNCount)
        """
        senistivity = 0
        """
            specificity        
            SPC = TNCount/(TNCount + FPCount)
        """
        specificity = 0
        """
            Statsitics on AU
        """
        AU_stat= {}
        for au in AU_list_initial:
            AU_stat[au] = {'correct':0,'incorrect':0,'total':0}
        for i,results in enumerate(y_pred):
#             print i, len(results)
            for i2,result in enumerate(results):
                AU = AU_list_initial[i2]
#                 print i2
#                 print '?????? ',
#                 print "AU" ,AU
#                 print "Evaluated result",result
#                 print "what we expect result to be",labels[i][AU+INDEX_ADJUST]
#                 print "all labels for case", labels[i][:-1]
                if 'EP' not in AU_stat[AU]:
                    AU_stat[AU]['EP'] = 0
                if 'EN' not in AU_stat[AU]:
                    AU_stat[AU]['EN'] = 0
                if 'TP' not in AU_stat[AU]:
                    AU_stat[AU]['TP'] = 0
                if 'TN' not in AU_stat[AU]:
                    AU_stat[AU]['TN'] = 0
                if 'FP' not in AU_stat[AU]:
                    AU_stat[AU]['FP'] = 0
                if 'FN' not in AU_stat[AU]:
                    AU_stat[AU]['FN'] = 0       
                if  labels[i][AU+INDEX_ADJUST] ==True:
                    AU_stat[AU]['EP'] += 1
                if labels[i][AU+INDEX_ADJUST] ==False:
                    AU_stat[AU]['EN'] += 1
                if result >= THRESHOLD and labels[i][AU+INDEX_ADJUST] ==True:
                    AU_stat[AU]['correct']+=1
                    AU_stat[AU]['TP'] += 1
                elif result < THRESHOLD and labels[i][AU+INDEX_ADJUST] ==False:
                    AU_stat[AU]['correct']+=1
                    AU_stat[AU]['TN'] += 1
                elif result < THRESHOLD and labels[i][AU+INDEX_ADJUST] ==True:
                    AU_stat[AU]['incorrect']+=1 
                    AU_stat[AU]['FN'] += 1
                elif result >= THRESHOLD and labels[i][AU+INDEX_ADJUST] ==False:
                    AU_stat[AU]['incorrect']+=1 
                    AU_stat[AU]['FP'] += 1
                else:
                    print '?????? ',
                    print "AU" ,AU
                    print "Evaluated result",result
                    print "what we expect result to be",labels[i][AU+INDEX_ADJUST]
                    print "all labels for case", labels[i]
                AU_stat[AU]['total']+=1
                #print AU_stat[AU]
        
        outputfile = open(os.path.join(results_folder,output_file.replace(".pickle","result")),"w")
        outputfile.write("Results for :" + file.replace("csv","result") +"\n")
        for k,v in AU_stat.items():
            #print k,v
            conf_mat = ConfusionMatrix(1,v['TP'],v['FP'],v['TN'],v['FN'],v['total'])
            result = conf_mat.performCalculations()
            au = k
            print "AU: %4s Precision: %0.4f Recall: %0.4f F-Score: %0.4f MSE: %0.4f RMSE: %0.4f Accuracy: %0.4f TPRate: %0.4f FPRate: %0.4f Specifity: %0.4f AUC: %0.4f"  \
                %(au, result.precision, result.recall, result.fScore, result.meanSquareError, result.rootMeanSquareError, result.accuracy,result.TPRate,result.FPRate,result.specificity,result.AUC)
            outputfile.write("AU:, %4s, Precision:, %0.4f, Recall:, %0.4f, F-Score:, %0.4f, MSE:, %0.4f, RMSE:, %0.4f, Accuracy:, %0.4f, TPRate:, %0.4f, FPRate:, %0.4f, Specifity:, %0.4f, AUC:, %0.4f, TP:, %4s, FP:, %4s, TN:, %4s, FN:, %4s, Total:, %4s, Actual Pos:, %4s, Actual Neg:, %4s, \n"  \
                %(au, result.precision, result.recall, result.fScore, result.meanSquareError, result.rootMeanSquareError, result.accuracy,result.TPRate,result.FPRate,result.specificity,result.AUC,v['TP'],v['FP'],v['TN'],v['FN'],v['total'],v['EP'],v['EN']))
        failure_rate = 0.0
        success_rate = 0.0
        items = 0
        for k,v in AU_stat.items():
            items += 1
            try:
                failure_rate += float(v['incorrect'])/float(v['total'])
                success_rate += float(v['correct'])/float(v['total'])
                AU_stat[k]['Success rate'] =  float(v['correct'])/float(v['total']) * 100
                AU_stat[k]['Failure rate'] =  float(v['incorrect'])/float(v['total']) *100
            except:
                pass
              
        # for k,v in AU_stat.items():
        #     print k ,v
        print "Failure rate: ",failure_rate/items *100
        print "Success rate: ",success_rate/items *100
        outputfile.write("Failure rate: "+str(failure_rate/items *100)+"\n")
        outputfile.write("Success rate: "+str(success_rate/items *100)+"\n")
        outputfile.close()
              
