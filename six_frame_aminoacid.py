#
/usr/bin/env python

import re
import sys

aa_dict = {
        'F':['TTT','TTC'],
        'L':['TTA','TTG','CTT','CTC','CTA','CTG'],
        'I':['ATT','ATC','ATA'],
        'M':['ATG'],
        'V':['GTT','GTC','GTA','GTG'],
        'S':['TCT','TCC','TCA','TCG'],
        'P':['CCT','CCC','CCA','CCG'],
        'T':['ACT','ACC','ACA','ACG'],
        'A':['GCT','GCC','GCA','GCG'],
        'Y':['TAT','TAC'],
        'H':['CAT','CAC'],
        'Q':['CAA','CAG'],
        'N':['AAT','AAC'],
        'K':['AAA','AAG'],
        'D':['GAT','GAC'],
        'E':['GAA','GAG'],
        'C':['TGT','TGC'],
        'W':['TGG'],
        'R':['CGT','CGC','CGA','CGG'],
        'S':['AGT','AGC'],
        'R':['AGA','AGG'],
        'G':['GGT','GGC','GGA','GGG']
        '-':['TAA','TAG','TGA']
        }


def split_input(string, chunk_size):
    """splits a string into a number of chunks of max length chunk_size"""
    num_chunks = len(string)/chunk_size
    if (len(string) % chunk_size != 0):
        num_chunks += 1
    output = []
    for i in range(0, num_chunks):
        output.append(string[chunk_size*i:chunk_size*(i+1)])
    return output

def translate(string):
    """translates a given nucleotide sequence into protein"""

