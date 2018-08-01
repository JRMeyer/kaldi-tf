# Josh Meyer // jrmeyer.github.io
#
# $ python3 egs-to-csv.py in-egs.txt out-egs.csv
#



import sys
import re


def extract_windows(eg, line, regex, outfile, win_size=62):
    '''
    given a line of labels, and the saved block of feature vectors,
    this function will extract windows of a given size and assign them
    to their label in a label -- flattened_data file
    win_size comes from the left and right context you provided to kaldi 
    to splice the frames
    '''

    # for each label in the nnet3Egs object
    for i, label in enumerate(regex.findall(line)):

        # cat all feats for that eg/label into a single vector
        catFeats=''
        for row in eg[i:i+win_size]:

            # remove the trailing \] if it exists (this is just a cleaning step)
            row = row[0].replace("]", "")
            # cat all the rows into one flat vector
            catFeats += (row + ' ')
            
        print(label, catFeats, file=outfile)


def get_eg_dim(arkfile):
    '''
    given kaldi ark file in txt format, find the dimension of the target labels
    '''
    with open(arkfile, "r") as arkf:
        for line in arkf:
            if "dim=" in line:
                egDim = re.search('dim=([0-9]*)', line).group(1)
                break
            else:
                pass

    return egDim




def main(arkfile, outfile):
    '''
    arkfile: is the input ark file from kaldi (egs.ark)
    regex: matches the labels of each eg based on number of dims in output layer
    outfile: where to save the output
    '''
    
    regex = re.compile("dim=[0-9]+ \[ ([0-9]+) ")
    
    eg=[]
    with open(arkfile,"r") as arkf:
        with open(outfile,"a") as outf:
            for line in arkf:
                # the first line of the eg
                if 'input' in line:
                    eg=[]
                    pass
                # if we've hit the labels then we're at the end of the data
                elif 'output' in line:
                    extract_windows(eg, line, regex, outf)
                    # this should be one frame of data
                else:
                    eg.append([line.strip()])
                


if __name__ == "__main__":
        
    # this is a kaldi nnet3Egs ark file which has been converted
    # to txt via nnet3-copy-egs
    arkfile=sys.argv[1]
    outfile=sys.argv[2]
    data_dir=sys.argv[3]

    # print the dimension of the arkfile to disk for downstream use
    with open(str(data_dir) + '/' + 'DIM','w') as dimfile:
        print(get_eg_dim(arkfile), file=dimfile)    

    # this regex matches the label for
    # each eg in a frame of egs (ie the
    # ark file contains groups of egs
    # which make sense for TDNN)


    main(arkfile, outfile)

    print("Extracted egs from " + arkfile + " and printed to " + outfile )
    
