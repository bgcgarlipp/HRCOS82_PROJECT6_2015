import os
"""
    Test/training split csv file location
"""
csv_split = {}
csv_split['BP4D'] = 'BP4D-training_training_test_split.csv'
csv_split_files = {}

au_files = []
count = 0

"""
    Dictonary of AU files for each dataset 
"""
AU_folders = {}
AU_folders['BP4D'] = os.path.join('../../databases', 'BP4D/aucoding')
#AU_folders['CK'] = os.path.join('../../databases', 'cohn-kanade/aucoding')
for data,AU_folder in AU_folders.items():

    for subdir, dirs, files in os.walk(AU_folder):
        for file in files:
            with open(os.path.join(AU_folder,file)) as input_file:
                for i, line in enumerate(input_file):
                    line_data = line.split(',')
                    au_files.append(file.replace('.csv','').replace('_','/')+'/'+line_data[0]+'.jpg')

for name,location in csv_split.items():
    csv_split_files[name]= {}
    f = open(location,'r')
    for line in f:
        col = line.split(',')
        csv_split_files[col[0]] = col[1][:-1]
        found = False
        info = col[0].split('/')
        if col[0] not in au_files:
            if col[0][0] == 0:
                if col[0][1:] not in au_files:
                    print col[0]
                    
                    print [a  for a in au_files if info[0]+'/'+info[1] in a ]
                    count += 1
            else:
                print col[0]
                print [a  for a in au_files if info[0]+'/'+info[1] in a]
                count += 1
print count
