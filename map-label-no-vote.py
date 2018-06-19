# Joshua Meyer 2018
#
# $ python3 egs-to-csv.py path/to/txt/egs.txt
#



import sys
import re



def replace_labels(curLine, newLabels, outfile):
    '''
    '''

    newLabels=[1, 2, 3, 4, 5, 6, 7, 8]

    # for each label in the nnet3Egs object
    line= re.split('(rows=. )', curLine)

    misc = line[0] + line[1]
    labels = line[2]

    i=0
    newOut=''
    for label in re.split('(dim=\d+ \[ \d+ \d+ \])', labels):
        if 'dim' in label:
            newLabel = re.sub('\[ \d+', '[ ' + str(newLabels[i]) , label)
            newOut+=newLabel
            i+=1
        else:
            newOut+=label # this should only be spaces

    print(curLine)
    print(misc+newOut)
            

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
    regex = re.compile("dim="+ get_eg_dim(arkfile) +" \[ ([0-9]*) ")
    
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
                


# if __name__ == "__main__":
        
#     # this is a kaldi nnet3Egs ark file which has been converted
#     # to txt via nnet3-copy-egs
#     arkfile=sys.argv[1] 

#     # this regex matches the label for
#     # each eg in a frame of egs (ie the
#     # ark file contains groups of egs
#     # which make sense for TDNN)


    
#     outfile="output.csv"
    
#     main(arkfile, outfile)

#     print("Extracted egs from " + arkfile + " and printed to " + outfile )
    



line='</NnetIo> <NnetIo> output <I1V> 8 <I1> 0 0 0 <I1> 0 1 0 <I1> 0 2 0 <I1> 0 3 0 <I1> 0 4 0 <I1> 0 5 0 <I1> 0 6 0 <I1> 0 7 0 rows=8 dim=736 [ 75 1 ] dim=736 [ 625 1 ] dim=736 [ 692 1 ] dim=736 [ 692 1 ] dim=736 [ 692 1 ] dim=736 [ 692 1 ] dim=736 [ 261 1 ] dim=736 [ 151 1 ]'

replace_labels(line, 'foo', 'bar')

# split string between rows and first dim
# save first half
# iterate over each dim, and replce with new label, catting to string
# cat first half of org string (up to row) with new labels
