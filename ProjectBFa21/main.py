# -*- coding: utf-8 -*-
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
'''just had to get the absolute path and make sure I'm properly reading the file'''
# import os
# THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
# my_file = os.path.join(THIS_FOLDER, 'apoe.txt')   

def main():
    dna = readFile('apoe.txt')
    complement = replication(dna)
    replication_file = 'replication.txt'
    writeFile(replication_file, complement)
    seq = 'CAGCTG' #seq to splice with
    enzyme = restriction(dna, seq)
    shortest_frag = ''.join(min(enzyme, key=len))
    #print(shortest_frag)
    '''just checking path'''
    # save_path = r'c:\Users\Vivek\Gateway Python\ProjectBFa21' 
    fragment_file = 'fragment.txt'
    #completeFile = os.path.join(save_path, new_file)
    writeFile(fragment_file, shortest_frag)

    mRNA = transcription(dna)
  
    codon_seq = translation(mRNA)
    '''writing codon text to just make sure it was working'''
    #codon_file = 'codon.txt'
    # writeFile(codon_file, ''.join(codon_seq))
    # print(len(''.join(codon_seq))%3)
    #print(codon_seq)
    
    #assigns higher or lower to risk and gives allele type to hidden variable risktype
    risk, risktype = allele(dna)
    # displays allele value using format
    print('This allele indicates a {} of Alzheimer\'s disease.'.format(risk))

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
    
    
def writeFile(fileName,text):
    """
    Writes a text file.

    Parameters
    ----------
    fileName : str
        File path to write.
    text : str
        Text to write.

    Returns
    -------
    None.

    """
    with open(fileName,'w') as textFile:
        textFile.write(text)

def flatten(matrix):
    """flatten nested list into standard list

    Args:
        matrix (list): nested list of spliced sequences

    Returns:
        list: vector list of cut sequences
    """    
    return [index for row in matrix for index in row]

def replication(dna):
    """returns complement of gene sequence

    Args:
        dna (str): sequences of nucleotides

    Returns:
        str: complement sequence of nucleotides
    """    
    complement = dna.replace("A", 't').replace("T", 'A').replace("C", "g").replace("G", "C").upper() 
    #replaces A, T, C, G with T, A, G, C respectively
    #had to do upper() because it would replace A with T and then replace the same T with A, so I had to differentiate with case
    return complement

def restriction(dna, seq):
    """[simulates restriction enzyme by slicing dna at midpoint of sequence]

    Args:
        dna ([str]): [sequence of nucleotides]
        seq ([str]): [restriction site]

    Returns:
        [list]: [returns list of spliced sequences]
    """    
    splice = len(seq) / 2 #find midpoint of site
    reduction = dna #copy of dna to cut through
    splicelist = [] #empty list to hold spliced sequences

    while seq in reduction:
        index = int(reduction.index(seq)) #finds index of first letter of seq
        site = int(index + splice) #adds splice to find midpoint
        parse1, reduction = reduction[:site], reduction[site:] #splits at site and makes reduction[site:] new string to search
        splicelist.append(parse1) #appends everything left of the site
    splicelist.append(reduction) #finally appends everything right of the last site
    return splicelist

def transcription(dna): 
    """converts dna into mrna

    Args:
        dna (str): sequence of nucleotides

    Returns:
        mrna (str) : sequence of nucleotides with thymine replaced with uracil
    """    
    mRNA = dna.replace('T', 'U') #replaces every T with U
    return mRNA

def translation(mrna): 
    """outputs amino acid sequence for mrna input

    Args:
        mrna (str): sequence of nucleotides with uracil instead of thymine

    Returns:
        str: sequence of amino acids with white space between each
    """    
    amino_acid = [] #empty list to hold amino acids
    codon = re.findall('.{3}', mrna) #runs through every 3 characters of sequence and generates list
    for seq in codon:
        amino_acid.append(codons[seq]) #replaces codon sequence with amino acid from codons dictionary
    AA = ' '.join(amino_acid) #joins everything with space between amino acid
    return AA

def allele(dna):
    """determines whether a particular gene sequence has a higher or lower risk of Alzheimer's

    Args:
        dna (str): sequence of nucleotides

    Returns:
        str: returns either 'higher risk' or 'lower risk'
        int: returns allele type (-1, 2, 3, 4) as hidden variable
    """    
    YYY = ''.join(re.findall('(.{3})GGCCGCCTGGTGCAGTACCGCGGC', dna)) 
    #runs through sequence until finding matching sequence including 3 preceding characters. 
    # removes space and only includes the 3 preceding characters
    ZZZ = ''.join(re.findall('(.{3})CTGGCAGTGTACCAGGCC', dna)) 
    #runs through sequence until finding matching sequence including 3 preceding characters. 
    # removes space and only includes the 3 preceding characters
    AAYYY = codons[transcription(YYY)] #replaces yyy with amino acid seq from codons dict
    AAZZZ = codons[transcription(ZZZ)] #replaces zzz with amino acid seq from codons dict
    if AAYYY == 'Arg' and AAZZZ == 'Arg': 
        #if amino acid yyy matches 'cys' AND amino acid zzz matches 'arg'
        #returns 'higher risk', else outputs 'lower risk'
        #returns hidden variable 4
        return 'higher risk', 4
    elif AAYYY == 'Cys' and AAZZZ == 'Cys': 
        #if yyy, zzz == cys, cys
        #returns lower risk and hidden var 2
        return 'lower risk', 2
    elif AAYYY == 'Cys' and AAZZZ == 'Arg': 
        #if yyy, zzz == cys, arg
        #returns lower risk and hidden var 3
        return 'lower risk', 3
    else:
        #if anything else
        #returns lower risk and hidden var -1
        return 'lower risk', -1
    

if __name__ == "__main__": 
    main()