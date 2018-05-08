import sys
import pandas
import tensorflow as tf


infile=sys.argv[1]
csv = pandas.read_csv(infile).values

with tf.python_io.TFRecordWriter("csv.tfrecords") as writer:
    for row in csv:
        features, label = row[1:], int(row[0])
        example = tf.train.Example()
        example.features.feature["features"].float_list.value.extend(features)
        example.features.feature["label"].int64_list.value.append(label)
        writer.write(example.SerializeToString())
