"""
    Basic python Imports
"""
import os
import csv
"""
    splitfiles location
"""
splitfolder = 'split_files'
"""
    CSV Folder location
"""
csv_folder = 'csv'
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
    folders done
"""
folders_done = []
"""
    Loop troough base data set folder and only create a dict entry for the data set and its resolution
"""
for subdir, dirs, files in os.walk(csv_folder):
    for file in files:
        print file
        checkfile = file.split('_')
        try:
            int(checkfile[len(checkfile)-2])
            newfilename = (checkfile[0]+"-"+checkfile[len(checkfile)-1]).replace('.csv','_split.csv')
            dataset = newfilename
        except:
            newfilename =(checkfile[0]+"-"+checkfile[len(checkfile)-2]+"_"+checkfile[len(checkfile)-1]).replace('.csv','_split.csv')
            dataset = newfilename
        if dataset not in folders_done:
            folders_done.append(dataset)
            new_csv = open(os.path.join(splitfolder,dataset),'w')
            with open(os.path.join(csv_folder,file), 'rb') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:
                    if '.jpg' in row[0]:
                        splitrow = row[0].split('/')
                        if 'train' in file:
                            new_csv.write(splitrow[len(splitrow)-3]+"/"+splitrow[len(splitrow)-2]+"/"+splitrow[len(splitrow)-1]+","+"training\n")
                        else:
                                                        new_csv.write(splitrow[len(splitrow)-3]+"/"+splitrow[len(splitrow)-2]+"/"+splitrow[len(splitrow)-1]+","+"test\n")
            new_csv.close()
                        
print folders_done
                    
        