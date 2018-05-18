import tensorflow as tf




  

def parser(record):
  features={
    'mfccs': tf.FixedLenFeature([], tf.string),
    'label': tf.FixedLenFeature([], tf.int64),
  }
  parsed = tf.parse_single_example(record, features)  
  mfccs= tf.convert_to_tensor(tf.decode_raw(parsed['mfccs'], tf.float64))
  label= tf.cast(parsed['label'], tf.int32)

  return {'mfccs': mfccs}, label


def my_input_fn(filepath='/home/ubuntu/csv.tfrecords'):
  dataset = tf.data.TFRecordDataset(filepath)
  dataset = dataset.map(parser)
  dataset = dataset.shuffle(buffer_size=256)
  dataset = dataset.batch(1)
  
  iterator = dataset.make_one_shot_iterator()

  batch_mfccs, batch_labels = iterator.get_next()

  return batch_mfccs, batch_labels


with tf.Session() as sess:
  feats, labs =sess.run(my_input_fn())
  print(len(feats), len(feats['mfccs'][0]))

# Create the feature_columns, which specifies the input to our model.
# All our input features are numeric, so use numeric_column for each one.
# I have 377 floats for each mfcc window
feature_columns = [tf.feature_column.numeric_column(key='mfccs', dtype=tf.float64, shape=(377,))]


# Use the DNNClassifier pre-made estimator
classifier = tf.estimator.DNNClassifier(
  feature_columns=feature_columns, # The input features to our model
  hidden_units=[10, 10], # Two layers, each with 10 neurons
  n_classes=96,
  model_dir='/tmp/') # Path to where checkpoints etc are stored



# Train our model, use the previously function my_input_fn
# Input to training is a file with training example
# Stop training after 8 iterations of train data (epochs)

with tf.Session() as sess:
  sess.run(
    classifier.train(
      input_fn=lambda: my_input_fn()
    )
  )

exit()                                                                                         

# def train_kmeans(batch):
#     kmeansEstimator = tf.contrib.factorization.KMeansClustering(num_clusters=1000, use_mini_batch=False)
#     kmeansEstimator.train(batch)
#     centers = kmeansEstimator.cluster_centers()
#     return centers
