import sys
import re



def extract_windows(eg, line, outfile, win_size=29):
    '''
    given a line of labels, and the saved block of feature vectors,
    this function will extract windows of a given size and assign them
    to their label in a label -- flattened_data file
    '''

    # for each label in the nnet3Egs object
    for i, label in enumerate(regex.findall(line)):

        # cat all feats for that eg/label into a single vector
        catFeats=''
        for row in eg[i:i+win_size]:
            catFeats += (row[0] + ' ')
            
        print(label, catFeats, file=outfile)






def main(arkfile, regex, outfile):
    '''
    arkfile: is the input ark file from kaldi (egs.ark)
    regex: matches the labels of each eg based on number of dims in output layer
    outfile: where to save the output
    '''
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
                    extract_windows(eg, line, outf)
                    # this should be one frame of data
                else:
                    eg.append([line.strip()])
                


if __name__ == "__main__":
        
    # this is a kaldi nnet3Egs ark file which has been converted
    # to txt via nnet3-copy-egs
    arkfile=sys.argv[1] 

    # this regex matches the label for
    # each eg in a frame of egs (ie the
    # ark file contains groups of egs
    # which make sense for TDNN)
    regex = re.compile("dim=96 \[ ([0-9]*) ") 

    outfile="output.csv"
    
    main(arkfile, regex, outfile)

    print("Extracted egs from " + arkfile + " and printed to " + outfile )
    
