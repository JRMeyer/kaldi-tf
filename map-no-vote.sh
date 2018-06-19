#!/bin/bash

ARKFILE=$1
LABELS=$2

i=0;
while read line; do

    case $line in
	*08113*)
	    
	    i=$((i+8))
	    
	    matches=$( head -$i $LABELS | tail -n8 )
	    for match in $matches;
	    do
		echo $match
	    done	 
	    echo 'HIT LINE' $i;

	    ;;
	
	*)
	    ;;
    esac;

done <$ARKFILE;
echo $i
