#!/bin/bash
# Josh Meyer // jrmeyer.github.io

echo "### SPLIT ARK FOR MULTIPLE JOBS ###"


ARKFILE=$1
MAPPINGS=$2
DIM=$3
TMP_DIR=$4


num_lines=(`wc -l $ARKFILE`)
num_processors=(`nproc`)
segs_per_job=$(( num_lines / num_processors ))

echo "$0: processing $num_lines segments from $ARKFILE"
echo "$0: splitting segments over $num_processors CPUs"
echo "$0: with $segs_per_job segments per job."
# will split into segments00 segments01 ... etc
split -l $segs_per_job --numeric-suffixes --additional-suffix=.tmp $ARKFILE $TMP_DIR/ARK_split





# make an array for proc ids
proc_ids=()

for i in $TMP_DIR/ARK_split*.tmp; do
    while read mapping; do
	mapArr=($mapping)
	old=${mapArr[0]}
	new=${mapArr[1]}
    sed_command=${sed -e "s/ \[ ${old} / \[ ${new}@ /g"}
	parallel --pipepart --block 5M -a $i -k 'sed -e "s/ \[ ${old} / \[ ${new}@ /g"' > ${i}.mod # without the underscores we double replace!!!!
    done <$MAPPINGS &
    proc_ids+=($!)
done

# wait for subprocesses to stop
for proc_id in ${proc_ids[*]}; do wait $proc_id; done;

rm ARK_split*.tmp

proc_ids=()
for i in $TMP_DIR/ARK_split*.mod; do
    parallel --pipepart --block 5M -a $i -k sed "s/@//g" > ${i}.tmp & # without the underscores we double replace!!!!
    proc_ids+=($!)
done


# wait for subprocesses to stop
for proc_id in ${proc_ids[*]}; do wait $proc_id; done;

rm ARK_split*.mod
