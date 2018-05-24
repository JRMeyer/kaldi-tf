import sys
import pandas
import tensorflow as tf
import numpy as np

# 
# USAGE: $ python3 csv-to-tfrecords.py data.csv data.tfrecords
#
#

infile=sys.argv[1]
outfile=sys.argv[2]

csv = pandas.read_csv(infile, header=None).values


with tf.python_io.TFRecordWriter(outfile) as writer:
    for row in csv:
        # row is read as a single char string, so remove trailing whitespace and split
        row = row[0].rstrip().split(' ')
        # the first col is label, all rest are feats
        label = int(row[0])

        mfccs = np.array([ float(feat) for feat in row[1:] ]).tostring()
        
        example = tf.train.Example()
        example.features.feature["mfccs"].bytes_list.value.append(mfccs)
        example.features.feature["label"].int64_list.value.append(label)
        writer.write(example.SerializeToString())
