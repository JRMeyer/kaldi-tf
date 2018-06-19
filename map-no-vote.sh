#!/bin/bash

ARKFILE=$1
LABELS=$2

i=0;
while read line; do

    case $line in
	*output*)
	    
	    i=$((i+8))
	    
	    matches=$( head -$i $LABELS | tail -n8 )
	    echo $matches
	    # for match in $matches;
	    # do
	    # 	echo $match
	    # done	 
	    echo 'HIT LINE' $i;

	    ;;
	
	*)
	    ;;
    esac;

done <$ARKFILE;
echo $i
