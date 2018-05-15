import numpy as np
import tensorflow as tf
import sys




def parser(record):
  features={
    'mfccs': tf.FixedLenFeature([], tf.string),
    'label': tf.FixedLenFeature([], tf.int64),
  }

  # # A `tf.data.Dataset` whose elements are dictionaries mapping feature names
  # # (in this case 'seq') to tensors, based on `features`.
  parsed = tf.parse_single_example(record, features)
  
  mfccs= tf.decode_raw(parsed['mfccs'], tf.float64)
  label= tf.cast(parsed['label'], tf.int32)
  
  return label, mfccs


def input_fn(filenames):
  
  dataset = tf.data.TFRecordDataset(filenames)
  dataset = dataset.map(parser)
  iterator = dataset.make_one_shot_iterator()
  label, mfccs = iterator.get_next()

  return label, mfccs
  

if __name__ == "__main__":

  # for example in tf.python_io.tf_record_iterator("/home/ubuntu/csv.tfrecords"):
      # result = tf.train.Example.FromString(example)
      # print(result)
      # exit()
  
  with tf.Session() as sess:
        label, mfccs = sess.run(input_fn('/home/ubuntu/csv.tfrecords'))
        print(label)




exit()

# https://medium.com/@TalPerry/getting-text-into-tensorflow-with-the-dataset-api-ffb832c8bec6
