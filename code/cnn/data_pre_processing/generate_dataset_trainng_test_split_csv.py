import os
from random import randint
"""
    Dataset information
    image_folder : base datasets folder
    datasets_to_process : subfolders in datasets to process
"""
images_folder = '../../databases'
"""
     How much do we want to train on in percetage has to be less than 100 
"""
training = 80
max = 100
datasets_to_process = ['cohn-kanade/images','BP4D/images']
"""
    Loops trough datasets 
"""
for dataset in datasets_to_process:
    datasetfile = open(dataset.replace('/','_')+"_training_test_split.csv",'w')
    for subdir, dirs, files in os.walk(os.path.join(images_folder,dataset)):
        for file in files:
            """
                split subdir into folders
            """
            folders = subdir.split('/')
            """
                Check split assigned and devides data set appopriately, added randint for some randomeness
            """
            if randint(0,max) < training:
                datasetfile.write(os.path.join(folders[len(folders)-2],folders[len(folders)-1],file)+",training\n")
            else:
                datasetfile.write(os.path.join(folders[len(folders)-2],folders[len(folders)-1],file)+",test\n")
    datasetfile.close()
