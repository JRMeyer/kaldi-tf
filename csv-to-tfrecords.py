import sys
import pandas
import tensorflow as tf


infile=sys.argv[1]
csv = pandas.read_csv(infile).values

with tf.python_io.TFRecordWriter("csv.tfrecords") as writer:
    for row in csv:
        # row is read as a single char string, so remove problems (the extra ]) and split
        row = row[0].replace("]","").rstrip().split(' ')
        # the first col is label, all rest are feats
        label = int(row[0])

        features = [ float(feat) for feat in row[1:] ]
        # create tf.example
        example = tf.train.Example()
        example.features.feature["features"].float_list.value.extend(features)
        example.features.feature["label"].int64_list.value.append(label)
        writer.write(example.SerializeToString())
