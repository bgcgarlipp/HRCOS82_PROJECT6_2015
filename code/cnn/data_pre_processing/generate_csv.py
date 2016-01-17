"""
    Basic python Imports
"""
import os
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as pyplot
import csv
from random import randint
import sys, traceback
from auUtils import locateFirstFile
"""
    Test/training split csv file location
"""
csv_split = {}
csv_split['BP4D'] = 'BP4D-training_training_test_split.csv'
csv_split['CK'] = 'cohn-kanade-images_training_test_split.csv'
csv_split_files = {}
"""
    Dictonary of AU files for each dataset 
"""
AU_folders = {}
AU_folders['BP4D'] = os.path.join('../../databases', 'BP4D/aucoding')
AU_folders['CK'] = os.path.join('../../databases', 'cohn-kanade/aucoding')
"""
    Gender folders only for BP4D
"""
gender_images ={'BP4D':{}}
gender_images['BP4D']['male'] = ['M001','M002','M003','M004','M005','M006','M007','M008','M009','M010','M011','M012','M013','M014','M015','M016','M017','M018']
gender_images['BP4D']['female'] = ['F001','F002','F003','F004','F005','F006','F007','F008','F009','F010','F011','F012','F013','F014','F015','F016','F017','F018','F019','F020','F021','F022','F023']
"""
    Race folders only for BP4D
"""
race_images = {'BP4D':{}}
race_images['BP4D']['african'] = ['F001','F011','F012','F022','F023','M003','M017']
race_images['BP4D']['asian'] = ['F002','F003','F005','F007','F009','F014',
                                'F015','F018','F021','M005','M008']
race_images['BP4D']['caucasian'] = ['F004','F006','F008','F010','F013','F016',
                                    'F017','F019','F020','M001','M002','M004',
                                    'M006','M007','M009','M010','M011','M012','M013',
                                    'M014','M015','M016','M018']
"""
    base dataset folder
"""
images_folder  = 'datasets'
"""
    AU List we want to evaluate
""" 
AU_list_initial = [1 ,2, 4, 6, 7, 10, 12, 14 ,15, 17, 23]
CK_AU_Headers = range(1,99) # same as BP4D
"""
    headers columns
"""
headers_list = []
set_header = True
"""
    Csv files dictoinary
"""
csv_files = {}
datasets = {}
"""
    If you only want to generate a subset of the database insert quantity of sets else make it None to take whole set  
"""
subset_training = None
subset_test = None
"""
    Loop troough base data set folder and only create a dict entry for the data set and its resolution
"""
for subdir, dirs, files in os.walk(images_folder):
    if 'X' in subdir:
        """
            Split the folder names to get information of dataset
        """
        folders = subdir.split('/')
        dataset_info = folders[1].split('_')
        dataset = dataset_info[0]
        pixels = dataset_info[1].split('X')[0]
        if dataset in datasets:
            if pixels not in  datasets[dataset]:
                datasets[dataset].append(pixels)
        else:
            datasets[dataset] = [pixels]

print datasets
"""
    Generate the corresponding CSV files
"""
def findMaxDigits(searchPath):
    fileName = locateFirstFile("*.jpg", searchPath)
    if (fileName == None):
        return 0
    else:
        return len( fileName )

for k,v in datasets.items():
    csv_files[k] = {}
    for pix in v:
        csv_files[k][k+'_'+pix+'X'+pix+'_test'] = csv.writer(open('csv/'+k+'_'+str(pix)+'_'+str(pix)+'_test.csv', 'w'), delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_files[k][k+'_'+pix+'X'+pix+'_train'] = csv.writer(open('csv/'+k+'_'+str(pix)+'_'+str(pix)+'_train.csv', 'w'), delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if k in gender_images:
            for gender,frame_list in gender_images[k].items():
                csv_files[k][k+'_'+pix+'X'+pix+'_'+gender+'_test'] = csv.writer(open('csv/'+k+'_'+str(pix)+'_'+str(pix)+"_"+gender+'_test.csv', 'w'), delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_files[k][k+'_'+pix+'X'+pix+'_'+gender+'_train'] = csv.writer(open('csv/'+k+'_'+str(pix)+'_'+str(pix)+"_"+gender+'_train.csv', 'w'), delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if k in race_images:
            for race,frame_list in race_images[k].items():
                csv_files[k][k+'_'+pix+'X'+pix+'_'+race+'_test'] = csv.writer(open('csv/'+k+'_'+str(pix)+'_'+str(pix)+"_"+race+'_test.csv', 'w'), delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_files[k][k+'_'+pix+'X'+pix+'_'+race+'_train'] = csv.writer(open('csv/'+k+'_'+str(pix)+'_'+str(pix)+"_"+race+'_train.csv', 'w'), delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)

print csv_files
"""
    Generate Dict to show which files should be test or training data
"""
for name,location in csv_split.items():
    csv_split_files[name]= {}
    f = open(location,'r')
    for line in f:
        col = line.split(',')
        csv_split_files[col[0]] = col[1][:-1]


"""
    Loop trough AU we want to process and add these files to the csv
"""

for data,AU_folder in AU_folders.items():
    filecount = 0
    added = 0
    notadded = 0
    if data == 'BP4D':
        for pix in datasets[data]:
            print "Processing ",data+'_'+pix+'X'+pix
            test_added={'normal':0}
            train_added = {'normal':0}
            for gender,frame_list in  gender_images[data].items():
                test_added[gender] = 0
                train_added[gender] = 0
            for race,frame_list in  race_images[data].items():
                test_added[race] = 0
                train_added[race] = 0
            set_header =True
            dataset_folder = data+'_'+pix+'X'+pix
            for subdir, dirs, files in os.walk(AU_folder):
                if subset_training is not None and subset_test is not None :
                    should_stop = True;
                    for item,value in test_added.items():
                        if value < subset_test:
                            should_stop = False
                    for item,value in train_added.items():
                        if value < subset_training:
                            should_stop = False
                    if should_stop:
                        print "Stoping ---------------"
                        break  
                for file in files:
                #print file
                    if subset_training is not None and subset_test is not None :
                        should_stop = True;
                        for item,value in test_added.items():
                            if value < subset_test:
                                should_stop = False
                        for item,value in train_added.items():
                            if value < subset_training:
                                should_stop = False
                        if should_stop:
                            print "Stoping ---------------"
                            break   
                    test_case = file.split("_")[1].replace('.csv','')
                    frame = file.split("_")[0]
                    with open(os.path.join(AU_folder,file)) as input_file:
                        for i, line in enumerate(input_file):
                            line_data = line.split(',')
                            should_not_add = False
                            if i == 0 and set_header:
                                line_data[0] = 'filename'
                                headers_list = line_data + ['Image']
                                """
                                    Normal headers
                                """
                                csv_files[data][data+'_'+pix+'X'+pix+'_test'].writerow(line_data + ['Image'])
                                csv_files[data][data+'_'+pix+'X'+pix+'_train'].writerow(line_data + ['Image'])
                                """
                                Gender Headers
                                """
                                for gender,frame_list in  gender_images[data].items():
                                        csv_files[k][data+'_'+pix+'X'+pix+'_'+gender+'_test'].writerow(line_data + ['Image'])
                                        csv_files[k][data+'_'+pix+'X'+pix+'_'+gender+'_train'].writerow(line_data + ['Image'])
                                """
                                Race Headers
                                """
                                for race,frame_list in  race_images[data].items():
                                    csv_files[k][data+'_'+pix+'X'+pix+'_'+race+'_test'].writerow(line_data + ['Image'])
                                    csv_files[k][data+'_'+pix+'X'+pix+'_'+race+'_train'].writerow(line_data + ['Image'])
                                set_header =False
                            else:
                                for AU in AU_list_initial:
                                    try:
                                        if line_data[AU] == 9:
                                            should_not_add= True
                                           # break
                                    except:
                                        pass
                                if not should_not_add:
                                    filecount += 1
                                    maxLength = findMaxDigits(os.path.join('datasets',dataset_folder, frame,test_case))
                                    orignal_filename = "{}.jpg".format(line_data[0]).rjust(maxLength, "0")
                                    
                                    img_filename =  os.path.join('datasets',dataset_folder, frame,test_case,orignal_filename)
                                    if os.path.join(frame,test_case,orignal_filename) not in csv_split_files:
                                        continue
                                    line_data[0] = img_filename
                                    image = cv2.imread(img_filename,0)
                                    #print img_filename
                                    if image is not None:
                                        output =  ' '.join(' '.join(str(cell) for cell in row) for row in image)
                                        
                                        if csv_split_files[os.path.join(frame,test_case,orignal_filename)] == 'test':
                                            """
                                            Normal test cases
                                            """
                                            if subset_test is not None and test_added['normal'] < subset_test:
                                                csv_files[k][data+'_'+pix+'X'+pix+'_test'].writerow(line_data+[output])
                                                test_added['normal'] +=1
                                                added +=1
                                            elif subset_test is None:
                                                csv_files[k][data+'_'+pix+'X'+pix+'_test'].writerow(line_data+[output])
                                                added +=1
                                            """
                                            Gender test cases
                                            """
                                            for gender,frame_list in  gender_images[data].items():
                                                if frame in frame_list:
                                                    if subset_test is not None and test_added[gender] < subset_test:
                                                        csv_files[k][data+'_'+pix+'X'+pix+'_'+gender+'_test'].writerow(line_data+[output])
                                                        test_added[gender] +=1
                                                        added +=1
                                                    elif subset_test is None:
                                                        csv_files[k][data+'_'+pix+'X'+pix+'_'+gender+'_test'].writerow(line_data+[output])
                                                        added +=1
                                            """
                                            Race test cases
                                            """
                                            for race,frame_list in  race_images[data].items():
                                                if subset_test is not None and test_added[race] < subset_test:
                                                    csv_files[k][data+'_'+pix+'X'+pix+'_'+race+'_test'].writerow(line_data+[output])
                                                    test_added[race] +=1
                                                    added +=1
                                                elif subset_test is None:
                                                    csv_files[k][data+'_'+pix+'X'+pix+'_'+race+'_test'].writerow(line_data+[output])
                                                    added +=1
                                        elif csv_split_files[os.path.join(frame,test_case,orignal_filename)] == 'training':              
                                            """
                                            Normal test cases
                                            """
                                            if subset_test is not None and train_added['normal'] < subset_training:
                                                csv_files[k][data+'_'+pix+'X'+pix+'_train'].writerow(line_data+[output])
                                                train_added['normal'] +=1
                                                added +=1
                                            elif subset_test is None:
                                                csv_files[k][data+'_'+pix+'X'+pix+'_train'].writerow(line_data+[output])
                                                added +=1
                                            """
                                            Gender test cases
                                            """
                                            for gender,frame_list in  gender_images[data].items():
                                                if frame in frame_list:
                                                    if subset_test is not None and train_added[gender] < subset_training:
                                                        csv_files[k][data+'_'+pix+'X'+pix+'_'+gender+'_train'].writerow(line_data+[output])
                                                        train_added[gender] +=1
                                                        added +=1
                                                    elif subset_test is None:
                                                        csv_files[k][data+'_'+pix+'X'+pix+'_'+gender+'_train'].writerow(line_data+[output])
                                                        added +=1
                                            """
                                            Race test cases
                                            """
                                            for race,frame_list in  race_images[data].items():
                                                if subset_test is not None and train_added[race] < subset_training:
                                                    csv_files[k][data+'_'+pix+'X'+pix+'_'+race+'_train'].writerow(line_data+[output])
                                                    train_added[race] +=1
                                                    added +=1
                                                elif subset_test is None:
                                                    csv_files[k][data+'_'+pix+'X'+pix+'_'+race+'_train'].writerow(line_data+[output])
                                                    added +=1
                                        
                                    else:
                                        notadded += 1
                                        print 'File None', img_filename
                                else:
                                    notadded += 1
                                    #print 'not Added AU == 9', img_filename
                            if subset_training is not None:
                                print data, " Added :", added , " not added ",notadded,'train_added ',str(train_added),'test_added',str(test_added) 
    elif data == 'CK':  

        """
            get the AU from ck+ database into dict
        """         
        subjects_AU = {}
        subjects_emotion = {}
        for subdir, dirs, files in os.walk(AU_folder):
            for file in files:
                folder =  subdir.split('/')
                AU_list = []
                f = open(os.path.join(subdir, file),'r')
                filedata = f.read()
                for line in filedata.split('\n'):
                        if len(line) > 0:
                            items = ""
                            values = ""
                            items = line.split('   ')
                            try:
                                    if 'e+' in items[1]:
                                        values = items[1].split('e+')
                                        AU_list.append(int(float(values[0])*10**float(values[1])))
                                    else:
                                        AU_list.append(int(float(values[0])*10**float(item[1])))
                            except Exception as e:
                                    print(e)
                                    print(line)
                                    print(items)
                                    print(values)
                                    print(os.path.join(subdir, file))
                                    print '-'*60
                                    traceback.print_exc(file=sys.stdout)
                                    print '-'*60
                subjects_AU[file.replace('_facs.txt',"")] = AU_list
        
        #print  subjects_AU  
        print datasets 
        for pix in datasets[data]:
            print "Processing ",data+'_'+pix+'X'+pix
            test_added = 0
            train_added = 0
            set_header =True
            dataset_folder = data+'_'+pix+'X'+pix
            """
                Add CSV headers
            """
            csv_files[data][data+'_'+pix+'X'+pix+'_test'].writerow(['filename'] + CK_AU_Headers +['Image'])
            csv_files[data][data+'_'+pix+'X'+pix+'_train'].writerow(['filename'] + CK_AU_Headers +['Image'])
            for subdir, dirs, files in os.walk(os.path.join('datasets',dataset_folder)):
                if subset_training is not None and subset_test is not None and test_added >= subset_test and   train_added >= subset_training:      
                    break   
                for file in files:
                    try:
                        folder =  subdir.split('/')
                        filename = file.replace('.png',"")
                        if filename in subjects_AU:
                            list = [False]*len(CK_AU_Headers)
                            for au in subjects_AU[filename]:
                                try:
                                    list[au-1] = True
                                except:
                                    pass
                            filecount += 1
                            orignal_filename = file
                            img_filename =  os.path.join(subdir,file)
                            image = cv2.imread(img_filename,0)
                            if image is not None:
                                output =  ' '.join(' '.join(str(cell) for cell in row) for row in image)
                                if csv_split_files[os.path.join(folder[len(folder)-2],folder[len(folder)-1],orignal_filename)] == 'test':
                                    if subset_test is not None and test_added < subset_test:
                                        csv_files[data][data+'_'+pix+'X'+pix+'_test'].writerow([file]+list+[output])
                                        test_added +=1
                                    elif subset_test is None:
                                        csv_files[data][data+'_'+pix+'X'+pix+'_test'].writerow([file]+list+[output])
                                elif csv_split_files[os.path.join(folder[len(folder)-2],folder[len(folder)-1],orignal_filename)] == 'training':   
                                    if  subset_training is not None and train_added < subset_training:
                                        train_added +=1      
                                        csv_files[data][data+'_'+pix+'X'+pix+'_train'].writerow([file]+list+[output])
                                    elif subset_training is  None:
                                        csv_files[data][data+'_'+pix+'X'+pix+'_train'].writerow([file]+list+[output])              
                                    
                            else:
                                pass
                                #print "Could not detect Face " + file
                        else:
                            pass
                            " Not all files have AU in CK +"
                            #print "file Not presenet " +filename

                    except Exception as e:
                        print "error " + str(e)
                        print '-'*60
                        traceback.print_exc(file=sys.stdout)
                        print '-'*60
