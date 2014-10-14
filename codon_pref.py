#!/usr/bin/env python

import re
import sys

class Seq(object):
    """Class string documentation"""

    aa_index = 0
    nuc_index = 0
    aa_dict = {
            'F':{'TTT':0,'TTC':0},
            'L':{'TTA':0,'TTG':0,'CTT':0,'CTC':0,'CTA':0,'CTG':0},
            'I':{'ATT':0,'ATC':0,'ATA':0},
            'M':{'ATG':0},
            'V':{'GTT':0,'GTC':0,'GTA':0,'GTG':0},
            'S':{'TCT':0,'TCC':0,'TCA':0,'TCG':0,'AGT':0,'AGC':0},
            'P':{'CCT':0,'CCC':0,'CCA':0,'CCG':0},
            'T':{'ACT':0,'ACC':0,'ACA':0,'ACG':0},
            'A':{'GCT':0,'GCC':0,'GCA':0,'GCG':0},
            'Y':{'TAT':0,'TAC':0},
            'H':{'CAT':0,'CAC':0},
            'Q':{'CAA':0,'CAG':0},
            'N':{'AAT':0,'AAC':0},
            'K':{'AAA':0,'AAG':0},
            'D':{'GAT':0,'GAC':0},
            'E':{'GAA':0,'GAG':0},
            'C':{'TGT':0,'TGC':0},
            'W':{'TGG':0},
            'R':{'CGT':0,'CGC':0,'CGA':0,'CGG':0,'AGA':0,'AGG':0},
            'G':{'GGT':0,'GGC':0,'GGA':0,'GGG':0},
            }


    def __init__(self, seq1, seq2):
        self.nuc_seq = seq1
        self.aa_seq = seq2

    def index_aa(self):
        return aa_index

    def incr_aa(self):
        aa_index += 1

    def index_nuc(self):
        return nuc_index

    def incr_nuc(self):
        nuc_index += 3

	def lookup_aa(self, i=aa_index, seq=aa_seq):
        for i, n in enumerate(seq):
            return n

    def lookup_nuc(self, i=nuc_index, seq=nuc_seq):
        for i, n in enumerate(seq):
            return [n:n+3]

	def check_codon(self):
        for codon in lookup_nuc(index_nuc):
            return codon

	def update_codons(self):
		pass

def all_equal(l):
    c = 0
    for c,c+1 in l:
        if lookup_aa(c) == lookup_aa(c+1):
            c += 1
            pass
        else:
            assert False
    return True


nuc_file = sys.argv[1]
prot_file = sys.argv[2]

with open(nuc_file, 'U') as f1, open(prot_file, 'U') as f2:
    nuc_dict = {}
    prot_dict = {}
    for curline in f1:
        if curline.startswith(">"):
            curline = curline.strip(">").strip("\n")
            ID = curline
            nuc_dict[ID] = ''
        else:
            curline = curline.strip("\n")
            nuc_dict[ID] += curline

     for curline in f2:
        if curline.startswith(">"):
            curline = curline.strip(">").strip("\n")
            ID = curline
            prot_dict[ID] = ''
        else:
            curline = curline.strip("\n")
            prot_dict[ID] += curline

    obj_list = []
    for a,b in enumerate(nuc_dict.keys(), prot_dict.keys()):
        if re.search(a, b):
            obj_list.append(Seq(nuc_dict.get(a), prot_dict.get(b))
        else:
            pass

    num = len(obj_list[0].aa_seq)
    reps = 0
    while reps < num:
        if all_equal(obj_list):
            for obj in obj_list:
                obj.update_codons()
                obj.incr_aa()
                obj.incr_nuc()
        else:
            if obj.lookup_aa() == '-':
                obj.incr_aa()
            else:
                obj.incr_aa()
                obj.incr_nuc()

"""
read in aligned nucleotide and protein seq files

parse each as per other programs

write a loop to initialize a new object for each sequence with the first full
word of the description line as the var name and the sequence as one of the
object's attributes

now the actual program part:
for each object, get the current amino acid for the index value
check each one against each other, if all of them match, get the associated
	codon used, and then add it to the codon usage variable
advance the index for the nucleotide sequence three

if the amino acids do not match, advance the index for the nucleotide sequence
	only if the current value is not '-'

no matter what though, advance the amino acid sequence index forward one

continue on in this manner until the end of each sequence is reached

write output to a file which has the sequence ID and the associated list of
	codons and the number of times they are used
"""
