#!/bin/bash
echo "Create Female BP4D database set"
python ../createBp4dCsv.py --cfg bp4f_female.cfg --cnt 3000 ../../../databases/BP4D/images ../../../databases/BP4D/aucoding data/bp4_female.csv

echo "Create Female BP4D database set"
python ../createBp4dCsv.py --cfg bp4f_male.cfg --cnt 3000 ../../../databases/BP4D/images ../../../databases/BP4D/aucoding data/bp4_male.csv

echo "Create African BP4D database set"
python ../createBp4dCsv.py --cfg bp4f_african.cfg --cnt 3000 ../../../databases/BP4D/images ../../../databases/BP4D/aucoding data/bp4_african.csv

echo "Create Asian BP4D database set"
python ../createBp4dCsv.py --cfg bp4f_asian.cfg --cnt 3000 ../../../databases/BP4D/images ../../../databases/BP4D/aucoding data/bp4_asian.csv

echo "Create Caucasian BP4D database set"
python ../createBp4dCsv.py --cfg bp4f_caucasian.cfg --cnt 3000 ../../../databases/BP4D/images ../../../databases/BP4D/aucoding data/bp4_caucasian.csv

echo "Create Full BP4D database set"
python ../createBp4dCsv.py --cfg bp4f_full.cfg --cnt 3000 ../../../databases/BP4D/images ../../../databases/BP4D/aucoding data/bp4_full.csv