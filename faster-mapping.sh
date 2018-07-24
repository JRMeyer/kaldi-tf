#!/bin/bash
# Josh Meyer // jrmeyer.github.io

echo "### SPLIT ARK FOR MULTIPLE JOBS ###"


ARKFILE=$1
MAPPINGS=$2
DIM=$3

# while read mapping; do
#     mapArr=($mapping)
#     old=${mapArr[0]}
#     new=${mapArr[1]}
#     sed -Ei "s/dim=${DIM} \[ ${old} 1 \]/dim=${DIM} \[ ${new} 1 \]/g" $ARKFILE
# done <$MAPPINGS &



num_lines=(`wc -l $ARKFILE`)
num_processors=(`nproc`)
segs_per_job=$(( num_lines / num_processors ))

echo "$0: processing $num_lines segments from $ARKFILE"
echo "$0: splitting segments over $num_processors CPUs"
echo "$0: with $segs_per_job segments per job."
# will split into segments00 segments01 ... etc
split -l $segs_per_job --numeric-suffixes --additional-suffix=.tmp $ARKFILE ARK_split





# make an array for proc ids
proc_ids=()

for i in ARK_split*.tmp; do
    while read mapping; do
	mapArr=($mapping)
	old=${mapArr[0]}
	new=${mapArr[1]}
	sed -Ei "s/dim=${DIM} \[ ${old} 1 \]/dim=${DIM} \[ ${new}@1 \]/g" $i  # without the underscores we double replace!!!!
    done <$MAPPINGS &
    proc_ids+=($!)
done

# wait for subprocesses to stop
for proc_id in ${proc_ids[*]}; do wait $proc_id; done;


proc_ids=()
for i in ARK_split*.tmp; do
    sed -Ei s'/@/ /g' $i & # without the underscores we double replace!!!!
    proc_ids+=($!)
done
# wait for subprocesses to stop
for proc_id in ${proc_ids[*]}; do wait $proc_id; done;

