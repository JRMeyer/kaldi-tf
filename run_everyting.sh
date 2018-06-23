#!/bin/bash
#
# this script should take in an ark file in txt form and return an arkfile
# in txt form

INARK=$1
OUTARK=$2

# EGS --> CSV

python3 egs-to-csv.py $INARK ark.csv
# Split data into train / eval / all
# I know this isn't kosher, but right
# now idc about eval, it's just a step
# in the scripts
cp ark.csv all.csv
mv ark.csv train.csv
tail -n500 all.csv > eval.csv

# CSV --> TFRECORDS


python3 csv-to-tfrecords.py all.csv all.tfrecords
python3 csv-to-tfrecords.py eval.csv eval.tfrecords
python3 csv-to-tfrecords.py train.csv train.tfrecords


# TRAIN K-MEANS

# returns tf-labels.txt
python3 train_and_eval.py


# VOTE FOR MAPPINGS

cut -d' ' -f1 all.csv > kaldi-labels.txt
paste -d' ' kaldi-labels.txt tf-labels.txt > combined-labels.txt
python3 vote.py combined-labels.txt > mapping.txt




# PERFORM MAPPING
cp $INARK tmp.arkfile
./faster-mapping.sh tmp.arkfile mapping.txt
cat ARK_split* > $OUTARK


# CLEAN-UP

rm tmp.arkfile ARK_split* mapping.txt kaldi-labels.txt tf-labels.txt combined-labels.txt all.csv eval.csv train.csv all.tfrecords eval.tfrecords train.tfrecords

echo "Your original Kaldi egs ($INARK) have been modified and save to $OUTARK"
