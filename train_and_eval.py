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


def my_input_fn(tfrecords_path):
  dataset = tf.data.TFRecordDataset(tfrecords_path)
  dataset = dataset.map(parser)
  dataset = dataset.shuffle(buffer_size=256)

  dataset = dataset.batch(1)
  
  iterator = dataset.make_one_shot_iterator()

  batch_mfccs, batch_labels = iterator.get_next()

  return batch_mfccs, batch_labels


# Create the feature_columns, which specifies the input to our model.
# I have 377 floats for each mfcc window
feature_columns = [tf.feature_column.numeric_column(key='mfccs', dtype=tf.float64, shape=(377,))]


# Use the DNNClassifier pre-made estimator
classifier = tf.estimator.DNNClassifier(
  feature_columns=feature_columns, # The input features to our model
  hidden_units=[10, 10], # Two layers, each with 10 neurons
  n_classes=96,
  model_dir='/tmp/tf') # Path to where checkpoints etc are stored



train_spec = tf.estimator.TrainSpec(input_fn = lambda: my_input_fn('/home/ubuntu/train.tfrecords') , max_steps=1000)
eval_spec = tf.estimator.EvalSpec(input_fn = lambda: my_input_fn('/home/ubuntu/eval.tfrecords') )

tf.estimator.train_and_evaluate(classifier, train_spec, eval_spec)



exit()                                                                                         


# def train_kmeans(batch):
#     kmeansEstimator = tf.contrib.factorization.KMeansClustering(num_clusters=1000, use_mini_batch=False)
#     kmeansEstimator.train(batch)
#     centers = kmeansEstimator.cluster_centers()
#     return centers
