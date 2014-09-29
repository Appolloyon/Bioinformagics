#!/usr/bin/env python

import re
import sys

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
    print codon_list
    for codon in codon_list:
        print codon
        for k in aa_dict.keys():
            if codon in aa_dict.get(k):
                print "key: %s" % k
                aa_string += k
                print aa_string
    keys = aa_dict.keys()
    print ";eys: %s" % keys
    print len(keys)
    print aa_dict.get('R')
    print aa_dict['R']
    return aa_string


infile = sys.argv[1]

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
    outfile_1 = basename + "_frame1.fa"
    outfile_2 = basename + "_frame2.fa"
    outfile_3 = basename + "_frame3.fa"

    with open(outfile_1, 'w') as o1, open(outfile_2, 'w') as o2,\
            open(outfile_3, 'w') as o3:
        for k in seqdict:
            s1 = seqdict.get(k).upper()
            print s1
            s2 = seqdict.get(k).upper()
            s2 = s2[1:len(s2)]
            print s2
            s3 = seqdict.get(k).upper()
            s3 = s3[2:len(s3)]
            print s3

            aa_1 = translate(s1)
            aa_2 = translate(s2)
            aa_3 = translate(s3)

            o1.write(">" + k + "_frame1" + "\n")
            for chunk in split_input(aa_1, 80):
                o1.write(chunk + "\n")

            o2.write(">" + k + "_frame2" + "\n")
            for chunk in split_input(aa_2, 80):
                o2.write(chunk + "\n")

            o3.write(">" + k + "_frame3" + "\n")
            for chunk in split_input(aa_3, 80):
                o3.write(chunk + "\n")
