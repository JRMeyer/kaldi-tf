# josh meyer jrmeyer.github.io
# 2018

#
# this script takes in a two-column file (i.e. mapping.txt)
# where the left column is the triphone id from kaldi and
# the right col is the new cluster id from tensorflow

import sys

mapping=sys.argv[1]



phoneMap={}
with open(mapping, 'r') as f:
    lines = f.readlines()
    for line in lines:
        
        phone = line.split()[0]
        cluster = line.split()[1]

        if cluster in phoneMap:
            if phone in phoneMap[cluster]:
                phoneMap[cluster][phone] = phoneMap[cluster][phone] + 1
            else:
                phoneMap[cluster][phone] = 1

        else:
            phoneMap[cluster] = {phone:1}

for item in phoneMap.items():
    print(item[0], item[1])
        
