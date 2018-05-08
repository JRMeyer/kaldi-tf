import numpy as np
import tensorflow as tf



data_path = 'csv.tfrecords'  # address to save the hdf5 file


def input_fn(features):
    return tf.train.limit_epochs(
        features['features'],
        num_epochs=1)

num_clusters=5
kmeans = tf.contrib.factorization.KMeansClustering(
    num_clusters=num_clusters,
    use_mini_batch=False)



with tf.Session() as sess:
    feature = {"features": tf.FixedLenFeature([], tf.float32),
               "label": tf.FixedLenFeature([], tf.int64)}

    # Create a list of filenames and pass it to a queue
    filename_queue = tf.train.string_input_producer([data_path], num_epochs=1)
    
    # Define a reader and read the next record
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
    
    # Decode the record read by the reader
    features = tf.parse_single_example(serialized_example, features=feature)



    # train
    num_iterations=10
    previous_centers=None
    for _ in range(num_iterations):
        kmeans.train(input_fn(features))
        
        cluster_centers = kmeans.cluster_centers()
        
        if previous_centers is not None:
            print('delta: ', cluster_centers - previous_centers)
            
            previous_centers = cluster_centers
            
        print('score:', kmeans.score(input_fn))
    print('cluster centers:', cluster_centers)
            






exit()


num_points = 100
dimensions = 2
points = np.random.uniform(0, 1000, [num_points, dimensions])


def input_fn():
    return tf.train.limit_epochs(
        tf.convert_to_tensor(points, dtype=tf.float32),
        num_epochs=1)


num_clusters=5
kmeans = tf.contrib.factorization.KMeansClustering(
    num_clusters=num_clusters,
    use_mini_batch=False)


# train
num_iterations=10
previous_centers=None
for _ in range(num_iterations):
    kmeans.train(input_fn)

    cluster_centers = kmeans.cluster_centers()
    
    if previous_centers is not None:
        print('delta: ', cluster_centers - previous_centers)

    previous_centers = cluster_centers

    print('score:', kmeans.score(input_fn))
print('cluster centers:', cluster_centers)


# map the input points to their clusters
cluster_indices = list(kmeans.predict_cluster_index(input_fn))

for i, point in enumerate(points):
    cluster_index = cluster_indices[i]
    center = cluster_centers[cluster_index]
    print('point:', point, 'is in cluster', cluster_index, 'centered at', center)
