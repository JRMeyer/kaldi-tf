# kaldi-tf
-----------------------

A set of scripts for getting data out of Kaldi and into TensorFlow.


## Pipeline

1) Generate Kaldi phoneme-level alignments (`*.ali`) via GMMs
2) Generate Kaldi nnet3 neural net example files (`egs.*.ark`) from alignments
3) Convert binary Nnet3Egs ark files to text ark files via `nnet3-copy-egs.cc` (Kaldi src)
4) Convert text ark file to csv via `egs-to-csv.py` (this repo)
5) Convert csv to tfrecords via `csv-to-tfrecords.py` (this repo)
6) Read tfrecords, train, and evaluate with `train_and_eval.py`