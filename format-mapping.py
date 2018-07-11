# Josh Meyer // jrmeyer.github.io

# This script fixes the problem that occurs if the TF clusters (their IDs) are
# larger than the dimensionality of the original Kaldi eg. this problem only shows up
# when you train the modified egs in Kaldi, and the new target IDs happen to be
# larger than the dims of the eg (dim=X [ ID 1 ])

import sys

oldMappings=sys.argv[1]
newMappings=sys.argv[2]

i=0
newMap={}
with open(oldMappings) as orgMap:
    for line in orgMap.readlines():
        clusterID = line.split()[1]
        if clusterID in newMap:
            pass
        else:
            i+=1
            newMap[clusterID]=i

with open(newMappings, 'w') as newFile:
    with open(oldMappings) as orgMap:
        for line in orgMap.readlines():
            kaldiID, clusterID = line.split()
            print(str(kaldiID) + ' ' + str(newMap[clusterID]), file=newFile )

