#!/usr/bin/env python

import re
import sys

class Seq(object):
    """Class string documentation"""

    aa_index = 0
    nuc_index = 0

    def __init__(self, seq1, seq2):
        self.nuc_seq = seq1
        self.aa_seq = seq2

    def index_aa(self):
        return aa_index
        aa_index += 1

    def index_nuc(self):
        return nuc_index
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

    for a,b in enumerate(nuc_dict.keys(), prot_dict.keys()):
        counter = 0
        seq_list = []
        if re.search(a, b):
            `counter` = Seq(nuc_dict.get(a), prot_dict.get(b)
            seq_list.append(`counter`)
            counter += 1


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
