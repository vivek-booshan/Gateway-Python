codons = {"UUU":"Phe", "UUC":"Phe", "UUA":"Leu", "UUG":"Leu",
          "UCU":"Ser", "UCC":"Ser", "UCA":"Ser", "UCG":"Ser",
          "UAU":"Tyr", "UAC":"Tyr", "UAA":"STOP", "UAG":"STOP",
          "UGU":"Cys", "UGC":"Cys", "UGA":"STOP", "UGG":"Trp",
          "CUU":"Leu", "CUC":"Leu", "CUA":"Leu", "CUG":"Leu",
          "CCU":"Pro", "CCC":"Pro", "CCA":"Pro", "CCG":"Pro",
          "CAU":"His", "CAC":"His", "CAA":"Gln", "CAG":"Gln",
          "CGU":"Arg", "CGC":"Arg", "CGA":"Arg", "CGG":"Arg",
          "AUU":"Ile", "AUC":"Ile", "AUA":"Ile", "AUG":"Met",
          "ACU":"Thr", "ACC":"Thr", "ACA":"Thr", "ACG":"Thr",
          "AAU":"Asn", "AAC":"Asn", "AAA":"Lys", "AAG":"Lys",
          "AGU":"Ser", "AGC":"Ser", "AGA":"Arg", "AGG":"Arg",
          "GUU":"Val", "GUC":"Val", "GUA":"Val", "GUG":"Val",
          "GCU":"Ala", "GCC":"Ala", "GCA":"Ala", "GCG":"Ala",
          "GAU":"Asp", "GAC":"Asp", "GAA":"Glu", "GAG":"Glu",
          "GGU":"Gly", "GGC":"Gly", "GGA":"Gly", "GGG":"Gly"}
import re
#use absolute path of file in current directory, need it cause I have diff workspaces open
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'apoe.txt')

def readFile(fileName):
    """
    Reads a text file.
    
    Parameters
    ----------
    fileName : str
        File path to read.

    Returns
    -------
    str
        Text from file.
    """
    with open(fileName,'r') as dnaFile:
        bases = dnaFile.readlines()
        
    return ''.join(bases)
    

dna = readFile(my_file)

''' RESTRICTION TEST

dna = bases
seq = 'CAGCTG'
splice = len(seq)/2
parse1, parse2 = seq[:int(splice)], seq[int(splice):]
#reduction = bases
splicelist = []
#print(parse1, parse2)
#x = re.findall(r'([ATGC].*AG)CT', dna, re.IGNORECASE)
# x = re.findall('([ACGT].*' + re.escape(parse1) + ')' + re.escape(parse2), dna, re.IGNORECASE)
# y = re.findall(re.escape(parse1) + '(' + re.escape(parse2) + '.*[ATGC])', dna, re.IGNORECASE)
# #y = re.findall(r'AG(CT.*[ATGC])', dna, re.IGNORECASE)
# print(x, y)


while 'CAGCTG' in dna:
    x = re.findall('([ACGT].*' + re.escape(parse1) + ')' + re.escape(parse2), dna, re.IGNORECASE)
    y = re.findall(re.escape(parse1) + '(' + re.escape(parse2) + '.*[ATGC])', dna, re.IGNORECASE)
    splicelist.append(y)
    dna = ''.join(x)
splicelist.append(x)
'''

'''transcription test'''
#
def allele(dna):
    YYY = re.findall('(.{3})GGCCGCCTGGTGCAGTACCGCGGC', dna) 
    ZZZ = re.findall('(.{3})CTGGCAGTGTACCAGGCC', dna)
    apoe = [YYY, ZZZ]
    print(apoe)
#allele(dna) 

def flatten(matrix):
    """flatten nested list into standard list

    Args:
        matrix (list): nested list of spliced sequences

    Returns:
        list: vector list of cut sequences
    """    
    return [index for row in matrix for index in row]

def restriction(dna, seq):
    """[simulates restriction enzyme by slicing dna at midpoint of sequence]

    Args:
        dna ([str]): [sequence of nucleotides]
        seq ([str]): [restriction site]

    Returns:
        [list]: [returns list of spliced sequences]
    """    
    splice = len(seq) / 2 #find midpoint of site
    parse1, parse2 = seq[:int(splice)], seq[int(splice):] #first half and second half of splice
    reduction = dna #copy of dna to cut through
    splicelist = [] #empty list to hold spliced sequences

    while seq in reduction: #while reduction still contains the site in the sequence
        x = re.findall('([ACGT].*' + re.escape(parse1) + ')' + re.escape(parse2), reduction, re.IGNORECASE) 
        #using RegEx by looking at an indefinite sequence of ACGT until it finds the last possible restriction site
        #then it only appends everything behind parse1 including parse1
        y = re.findall(re.escape(parse1) + '(' + re.escape(parse2) + '.*[ATGC])', reduction, re.IGNORECASE)
        #using RegEx, looks for indefinite sequence of ACGT until it finds the last possible restriction site
        #then it only appends everything after parse2 including parse2 
        splicelist.append(y)
        #appends y to the list
        reduction = ''.join(x)
        #makes reduction equal to x so the sequence gets shorter everytime until there are no more restriction sites to cut
    splicelist.append(x)
    #splicelist = flatten(splicelist)
    #flatten splicelist from nested list to list
    if seq in str(splicelist[0]):
            while seq in str(splicelist[0]):
                x = re.findall('([ACGT].*' + re.escape(parse1) + ')' + re.escape(parse2), str(splicelist[0]), re.IGNORECASE) 
                y = re.findall(re.escape(parse1) + '(' + re.escape(parse2) + '.*[ATGC])', str(splicelist[0]), re.IGNORECASE)
                splicelist[0] = y
                print(x)
                print(y)
                #print(splicelist)
    #finally appends x to splicelist
    #flatten splicelist from nested list to list
    splicelist = flatten(splicelist)
    print(splicelist)
    return splicelist[::-1]
    #return reverse of splicelist because I append sequences from last to first

def restriction2(dna, seq):
    splice = len(seq) / 2 #find midpoint of site
    reduction = dna #copy of dna to cut through
    splicelist = [] #empty list to hold spliced sequences
    
    while seq in reduction:
        index = int(reduction.index(seq))
        site = int(index + splice)
        parse1, reduction = reduction[:site], reduction[site:]
        splicelist.append(parse1)
    splicelist.append(reduction)
    return splicelist

test = 'TAAAAGATATCCTGATATCAGCTTG'
seq = 'CAGCTG'

# enzyme = restriction(dna, seq)
# '\n\n'.join(enzyme)
enzyme2 = restriction2(dna, seq)
print(min(enzyme2, key=len))
