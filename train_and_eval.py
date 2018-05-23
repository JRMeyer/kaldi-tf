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


def my_input_fn(tfrecords_path, model):
  dataset = (
    tf.data.TFRecordDataset(tfrecords_path)
    .map(parser)
    .shuffle(buffer_size=5000)
    .batch(32)
  )
  
  iterator = dataset.make_one_shot_iterator()

  batch_mfccs, batch_labels = iterator.get_next()

  if model == "dnn":
    output = (batch_mfccs, batch_labels)
  elif model == "kmeans":
    output = batch_mfccs
    
  return output



def zscore(in_tensor):
  '''
  Some normalization for audio feats
  (value − min_value) / (max_value − min_value)
  '''
  out_tensor = tf.div(
    tf.subtract(
      in_tensor,
      tf.reduce_min(in_tensor)
    ),
    tf.subtract(
      tf.reduce_max(in_tensor),
      tf.reduce_min(in_tensor)
    )
  )
  return(out_tensor)

  

# K-Means

train_spec_kmeans = tf.estimator.TrainSpec(input_fn = lambda: my_input_fn('/home/ubuntu/csv.tfrecords', 'kmeans') , max_steps=500)
eval_spec_kmeans = tf.estimator.EvalSpec(input_fn = lambda: my_input_fn('/home/ubuntu/eval.tfrecords', 'kmeans') )

KMeansEstimator = tf.contrib.factorization.KMeansClustering(
  num_clusters=96,
  feature_columns = [tf.feature_column.numeric_column(
    key='mfccs',
    dtype=tf.float64,
    shape=(377,),
    normalizer_fn =  lambda x: zscore(x)
  )], # The input features to our model
  use_mini_batch=True)

print("Train and Evaluate K-Means")
tf.estimator.train_and_evaluate(KMeansEstimator, train_spec_kmeans, eval_spec_kmeans)

# map the input points to their clusters
cluster_centers = KMeansEstimator.cluster_centers()
cluster_indices = list(KMeansEstimator.predict_cluster_index(input_fn = lambda: my_input_fn('/home/ubuntu/eval.tfrecords', 'kmeans')))
for i in cluster_indices:
  print(i)




# # DNN

# # Define train and eval specs
# train_spec_dnn = tf.estimator.TrainSpec(input_fn = lambda: my_input_fn('/home/ubuntu/train.tfrecords', 'dnn') , max_steps=100000)
# eval_spec_dnn = tf.estimator.EvalSpec(input_fn = lambda: my_input_fn('/home/ubuntu/eval.tfrecords', 'dnn') )

# DNNClassifier = tf.estimator.DNNClassifier(
#   feature_columns = [tf.feature_column.numeric_column(key='mfccs', dtype=tf.float64, shape=(377,))], # The input features to our model
#   hidden_units = [256, 256, 256, 256], # Two layers, each with 10 neurons
#   n_classes = 96,
#   model_dir = '/tmp/tf') # Path to where checkpoints etc are stored



# print("Train and Evaluate DNN")
# tf.estimator.train_and_evaluate(DNNClassifier, train_spec_dnn, eval_spec_dnn)

# predictions = list(DNNClassifier.predict(input_fn = lambda: my_input_fn('/home/ubuntu/eval.tfrecords', 'dnn')))

# for logits in predictions:
#   print(logits['probabilities'])
  

