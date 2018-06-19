#!/bin/bash
# Joshua Meyer 2018

# given new mappings (a 2-col txt file)
#       old kaldi ark file (in txt format)
#
# search replace via sed


MAPPINGS=$1
TXTARK=$2

while read mapping; do
    mapArr=($mapping)
    old=${mapArr[0]}
    new=${mapArr[1]}

    sed -Ei "s/dim=736 \[ ${old} 1 \]/dim=736 \[ ${new} 1 \]/g" $TXTARK

done <$MAPPINGS
