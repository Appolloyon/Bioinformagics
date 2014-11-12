#!/usr/bin/env python

"""
Changelog
---------
Created: September 26, 2014
Last Updated: November 11, 2014
"""

import argparse

parser = argparse.ArgumentParser(
    description = """Translates a series of FASTA formatted nucleotide
        sequences into amino acid sequences in every possible
        reading frame.""",
    epilog = """Codon table is for standard sequences, other sequences
        can be accomodated by pasting in a different table.  Frame4 is
        minus frame1, frame5 minus frame2, etc.""")
parser.add_argument('infiles', nargs='+', help='list of infiles')
args = parser.parse_args()

# global codon table placed at top for ease of reference
aa_dict = {
        'F':['TTT','TTC'],
        'L':['TTA','TTG','CTT','CTC','CTA','CTG'],
        'I':['ATT','ATC','ATA'],
        'M':['ATG'],
        'V':['GTT','GTC','GTA','GTG'],
        'S':['TCT','TCC','TCA','TCG','AGT','AGC'],
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
        'R':['CGT','CGC','CGA','CGG','AGA','AGG'],
        'G':['GGT','GGC','GGA','GGG'],
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

def translate(string, aa_dict=aa_dict):
    """translates a given nucleotide sequence into protein"""
    aa_string = ''
    codon_list = []
    codon_num = len(string)/3
    if (len(string) % 3 != 0):
        codon_num += 1
    for i in range(0, codon_num):
        codon_list.append(string[3*i:3*(i+1)])
    for codon in codon_list:
        for k in aa_dict.keys():
            if codon in aa_dict.get(k):
                aa_string += k
    return aa_string

def complement(string):
    """minus frames require reverse complementation"""
    compstr = ''
    for nuc in string:
        if nuc == 'A':
            compstr += 'T'
        elif nuc == 'T':
            compstr += 'A'
        elif nuc == 'C':
            compstr += 'G'
        else:
            compstr += 'C'
    return compstr


for infile in args.infiles:
    with open(infile, 'U') as f:
        seqdict={}
        for curline in f:
            if curline.startswith(">"):
                curline=curline.strip(">").strip('\n')
                ID = curline
                seqdict[ID] = ''
            else:
                curline=curline.strip('\n')
                seqdict[ID] += curline

        name_list = infile.split('.')
        basename = name_list[0]
        out1 = basename + "_frame1.fa"
        out2 = basename + "_frame2.fa"
        out3 = basename + "_frame3.fa"
        #frames higher than 3 are minus reading frames
        out4 = basename + "_frame4.fa"
        out5 = basename + "_frame5.fa"
        out6 = basename + "_frame6.fa"

        with open(out1, 'w') as o1, open(out2, 'w') as o2, open(out3, 'w') as o3,\
            open(out4, 'w') as o4, open(out5, 'w') as o5, open(out6, 'w') as o6:
            for k in seqdict:
                s1 = seqdict.get(k).upper()
                s2 = s1[1:len(s1)]
                s3 = s1[2:len(s1)]
                #minus frames require reverse complementation
                s4 = complement(s1[::-1])
                s5 = s4[1:len(s4)]
                s6 = s4[2:len(s4)]

                aa1 = translate(s1)
                aa2 = translate(s2)
                aa3 = translate(s3)
                aa4 = translate(s4)
                aa5 = translate(s5)
                aa6 = translate(s6)

                o1.write(">" + k + "_frame1" + "\n")
                for chunk in split_input(aa1, 80):
                    o1.write(chunk + "\n")

                o2.write(">" + k + "_frame2" + "\n")
                for chunk in split_input(aa2, 80):
                    o2.write(chunk + "\n")

                o3.write(">" + k + "_frame3" + "\n")
                for chunk in split_input(aa3, 80):
                    o3.write(chunk + "\n")

                o4.write(">" + k + "_frame4" + "\n")
                for chunk in split_input(aa4, 80):
                    o4.write(chunk + "\n")

                o5.write(">" + k + "_frame5" + "\n")
                for chunk in split_input(aa5, 80):
                    o5.write(chunk + "\n")

                o6.write(">" + k + "_frame6" + "\n")
                for chunk in split_input(aa6, 80):
                    o6.write(chunk + "\n")
