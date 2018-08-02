#!/bin/bash
# Josh Meyer // jrmeyer.github.io

echo "### SPLIT ARK FOR MULTIPLE JOBS ###"


ARKFILE=$1
MAPPINGS=$2
TMP_DIR=$3



#### MANUAL SHARD ####

num_lines=(`wc -l $ARKFILE`)
num_processors=(`nproc`)
segs_per_job=$(( num_lines / num_processors ))

echo "$0: processing $num_lines segments from $ARKFILE"
echo "$0: splitting segments over $num_processors CPUs"
echo "$0: with $segs_per_job segments per job."

# will split into segments00 segments01 ... etc
split -l $segs_per_job --numeric-suffixes --additional-suffix=.tmp $ARKFILE $TMP_DIR/ARK_split

proc_ids=() # make an array for proc ids

for i in $TMP_DIR/ARK_split*.tmp; do
    while read mapping; do
	mapArr=($mapping)
	old=${mapArr[0]}
	new=${mapArr[1]}
        sed_command="s/ \[ ${old} / \[ ${new}@ /g"
        parallel --pipepart --block 500M -a $i -k sed -e \" $sed_command \" > ${i}.mod
        mv ${i}.mod $i
    done <$MAPPINGS &
    proc_ids+=($!)
done
# # wait for subprocesses to stop
for proc_id in ${proc_ids[*]}; do wait $proc_id; done;

###########

proc_ids=()
for i in $TMP_DIR/ARK_split*.tmp; do
    parallel --pipepart --block 500M -a $i -k 'sed "s/@//g"' > ${i}.final
    mv ${i}.final $i & 
    proc_ids+=($!)
done

# wait for subprocesses to stop
for proc_id in ${proc_ids[*]}; do wait $proc_id; done;

