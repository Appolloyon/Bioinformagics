#!/usr/bin/env python

"""
This program should be able to compare a transcript and genomic sequence
and return a count of edited sites in the form of a string where a zero
indicates no editing at that site and a one represents the site is edited.
Intended to be used with a later program to plot out the significance
of editing in the transcript.
"""

#import os
import sys
import re
import pylab

file_list = sys.argv[1:]

def nonblank_lines(f):
    for l in f:
        line = l.strip('\n')
        if line:
            yield line

def calc_zscore(string, start, end):
    chars = string[start:end]
    sum = 0.0
    for char in chars:
        sum += float(char)
    zscore = float((sum - (15*0.05))/((15*0.05*0.95)**0.5))
    return zscore

def get_indices(string):
    indices = []
    for i in range(len(string)):
        try:
            index_low = i
            index_high = i+15
            indices.append([index_low, index_high])
        except(ValueError,IndexError):
            pass
    return indices

for file in file_list:
    with open(file,'U') as f:
        seqdict={}
        for curline in nonblank_lines(f):
            curline = curline.strip('\n')
            if curline.startswith(">"):
                curline = curline.strip(">")
                ID = curline
                seqdict[ID] = ''
            else:
                seqdict[ID] += curline

for k in seqdict.keys():
    if re.search('genomic', k):
        seq1 = seqdict.get(k)
    elif re.search('transcript', k):
        seq2 = seqdict.get(k)
    else:
        pass

compstr = ''
for i, (res1, res2) in enumerate(zip(seq1, seq2)):
    if (res1 == '-' or res2 == '-') or res1 == res2:
         compstr += str(0)
    elif res1 != res2:
        compstr += str(1)
    else:
        pass

#print compstr
#with open("editing_out.csv", 'w') as o:
#    for char in compstr:
#        o.write(char + ',' + '\n')

#indices = get_indices(compstr)
#print indices

zlist = []
for s,e in get_indices(compstr):
    try:
        zlist.append(calc_zscore(compstr, s, e))
    except(ValueError,IndexError):
        pass

#print zlist
pylab.plot([z for z in zlist])
pylab.show()
