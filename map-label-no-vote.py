# Josh Meyer // jrmeyer.github.io
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

    
    return misc+newOut
            




def main(arkfile, new_label_file, outfile):
    '''
    arkfile: is the input ark file from kaldi (egs.ark)
    regex: matches the labels of each eg based on number of dims in output layer
    outfile: where to save the output
    '''
    
    
    with open(arkfile,"r") as arkf:
        for line in arkf:
            if 'output' in line:
                newLine = replace_labels(line, 'foo', 'bar')
                print(newLine)
            else:
                print(line)
                

                
if __name__ == "__main__":
        
    # this is a kaldi nnet3Egs ark file which has been converted
    # to txt via nnet3-copy-egs
    arkfile=sys.argv[1] 
    newLabels=sys.argv[2]
    
    # this regex matches the label for
    # each eg in a frame of egs (ie the
    # ark file contains groups of egs
    # which make sense for TDNN)


    
    
    main(arkfile, 'newlabs', 'out')




# line='</NnetIo> <NnetIo> output <I1V> 8 <I1> 0 0 0 <I1> 0 1 0 <I1> 0 2 0 <I1> 0 3 0 <I1> 0 4 0 <I1> 0 5 0 <I1> 0 6 0 <I1> 0 7 0 rows=8 dim=736 [ 75 1 ] dim=736 [ 625 1 ] dim=736 [ 692 1 ] dim=736 [ 692 1 ] dim=736 [ 692 1 ] dim=736 [ 692 1 ] dim=736 [ 261 1 ] dim=736 [ 151 1 ]'

# replace_labels(line, 'foo', 'bar')




# split string between rows and first dim
# save first half
# iterate over each dim, and replce with new label, catting to string
# cat first half of org string (up to row) with new labels
