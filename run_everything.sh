#!/bin/bash

# Josh Meyer // jrmeyer.github.io

#
# this script should take in an ark file in txt form and return an arkfile
# in txt form



# given the name of the experiment, this script assumes file structure
# that I've got set up
exp_name=${1}
tmp_dir="/data/TMP"
path_to_exp="/home/ubuntu/kaldi/egs/multi-task-kaldi/mtk/MTL/exp/${exp_name}/nnet3/egs"



if [ 1 ]; then
    echo "### CONVERTING BINARY EGS TO TEXT ###"
    echo "LOOKING FOR EGS IN ${path_to_exp}"
    # binary --> text
    KALDI=/home/ubuntu/kaldi/src/nnet3bin/nnet3-copy-egs
    $KALDI ark:${path_to_exp}/egs.1.ark ark,t:${tmp_dir}/org-txt-ark
    $KALDI ark:${path_to_exp}/valid_diagnostic.egs ark,t:${tmp_dir}/valid-txt-ark
    $KALDI ark:${path_to_exp}/train_diagnostic.egs ark,t:${tmp_dir}/train-txt-ark
    $KALDI ark:${path_to_exp}/combine.egs ark,t:${tmp_dir}/combine-txt-ark
fi



if [ 1 ]; then
    echo "### CONVERT EGS TO TFRECORDS  ###"
    # EGS --> CSV
    
    python3 egs-to-csv.py ${tmp_dir}/org-txt-ark ${tmp_dir}/ark.csv
    # Split data into train / eval / all
    # I know this isn't kosher, but right
    # now idc about eval, it's just a step
    # in the scripts
    
    cp ${tmp_dir}/ark.csv ${tmp_dir}/all.csv
    mv ${tmp_dir}/ark.csv ${tmp_dir}/train.csv
    tail -n100 ${tmp_dir}/all.csv > ${tmp_dir}/eval.csv
    # CSV --> TFRECORDS
    python3 csv-to-tfrecords.py ${tmp_dir}/all.csv ${tmp_dir}/all.tfrecords
    python3 csv-to-tfrecords.py ${tmp_dir}/eval.csv ${tmp_dir}/eval.tfrecords
    python3 csv-to-tfrecords.py ${tmp_dir}/train.csv ${tmp_dir}/train.tfrecords
    # TRAIN K-MEANS
    echo "### TRAIN AND EVAL MODEL  ###"
    echo "# remove old model in /tmp/tf"
    rm -rf /tmp/tf
    time python3 train_and_eval.py $tmp_dir    ## returns tf-labels.txt
fi


# VOTE FOR MAPPINGS
if [ 1 ]; then
    cut -d' ' -f1 ${tmp_dir}/all.csv > ${tmp_dir}/kaldi-labels.txt
    paste -d' ' ${tmp_dir}/kaldi-labels.txt ${tmp_dir}/tf-labels.txt > ${tmp_dir}/combined-labels.txt
    python3 vote.py ${tmp_dir}/combined-labels.txt > ${tmp_dir}/mapping.txt
    python3 format-mapping.py ${tmp_dir}/mapping.txt ${tmp_dir}/formatted-mapping.txt
fi



if [ 1 ]; then
    # PERFORM MAPPING
     for egs in org-txt-ark valid-txt-ark train-txt-ark combine-txt-ark;  do
 	./faster-mapping.sh $tmp_dir/$egs $tmp_dir/formatted-mapping.txt ${tmp_dir}
	cat ${tmp_dir}/ARK_split* > ${tmp_dir}/${egs}.mod
	rm ${tmp_dir}/ARK_split* 
    done
fi


if [ 1 ]; then
    echo "TXT.egs --> BIN.egs ;; RENAME AND MOVE BIN.egs"  
    # text --> binary
    
    $KALDI ark,t:${tmp_dir}/org-txt-ark.mod ark,scp:${tmp_dir}/egs.1.ark,${tmp_dir}/egs.scp
    $KALDI ark,t:${tmp_dir}/valid-txt-ark.mod ark,scp:${tmp_dir}/valid_diagnostic.egs,${tmp_dir}/valid_diagnostic.scp
    $KALDI ark,t:${tmp_dir}/train-txt-ark.mod ark,scp:${tmp_dir}/train_diagnostic.egs,${tmp_dir}/train_diagnostic.scp
    $KALDI ark,t:${tmp_dir}/combine-txt-ark.mod ark,scp:${tmp_dir}/combine.egs,${tmp_dir}/combine.scp
    
    # fix paths
    fix_path="s/\/data\/TMP/MTL\/exp\/${exp_name}\/nnet3\/egs/g"
    sed -Ei $fix_path ${tmp_dir}/*.scp
    
    # move old egs to tmp dir
    mkdir ${path_to_exp}/org-scp-ark
    mv ${path_to_exp}/*.scp ${path_to_exp}/*.ark ${path_to_exp}/*.egs ${path_to_exp}/org-scp-ark/.

    # move new to org dir
    mv ${tmp_dir}/*.scp ${tmp_dir}/*.ark ${tmp_dir}/*.egs ${path_to_exp}/.
    
    echo "### OLD ARKS and SCPs moved to ${path_to_exp}/org-scp-ark/"
    echo "### NEW ARKS just renamed to standard names"
fi


rm $tmp_dir/*


