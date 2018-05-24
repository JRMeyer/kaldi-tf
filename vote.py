import sys
import collections

# this script expects as input a single text file with two columns
# where the first column is a list of phoneme labels from kaldi
# and the second column is a list of cluster labels from tensorflow
# one row represents one window of audio from a kaldi nnet3Eg


infile=sys.argv[1]

with open(infile) as f:
    content = f.readlines()

vote_dict={}
for line in content:
    kaldi_label, tf_label = line.split()
    
    if kaldi_label in vote_dict:
        vote_dict[kaldi_label].append(tf_label)
    else:
        vote_dict[kaldi_label] = [tf_label]

for kaldi_label, tf_labels in vote_dict.items():
    most_common_tf_label = max(set(tf_labels), key=tf_labels.count)
    # just keep most common
    vote_dict[kaldi_label] = most_common_tf_label


for kaldi, tf in collections.OrderedDict(sorted(vote_dict.items())).items():
    print(kaldi, tf)
