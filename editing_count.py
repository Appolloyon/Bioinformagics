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

window_size = float(sys.argv[1])
file_list = sys.argv[2:]

def nonblank_lines(f):
    for l in f:
        line = l.strip('\n')
        if line:
            yield line

def calc_zscore(string, start, end, window_size, mean):
    chars = string[start:end]
    sum = 0.0
    m = mean
    w = window_size
    for char in chars:
        sum += float(char)
    zscore = float((sum - (w*m))/((w*m*(1-m))**0.5))
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

def gulp(string, start, gulp_size):
    gulpstr = ''
    chars = string[start:start+gulp_size]
    for char in chars:
        gulpstr += char
    return gulpstr

def calc_mean(string):
    sum = 0.0
    for d in string:
        d = float(d)
        sum += d
    mean = sum/(float(len(string)))
    return mean

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

index = 1
for k in seqdict.keys():
    print k
    try:
        exec("seq%d = '%s'" % (index, seqdict.get(k)))
    except(ValueError,IndexError):
        pass
    index += 1

i = 0
while gulp(seq1, i, 3) != gulp(seq2, i, 3):
    i += 1
    #print i

j = 0
while gulp(seq1[::-1], j, 3) != gulp(seq2[::-1], j, 3):
    j += 1
#print i
newseq1 = seq1[i:(len(seq1)-j)]
newseq2 = seq2[i:(len(seq2)-j)]

compstr = ''
for i, (res1, res2) in enumerate(zip(newseq1, newseq2)):
    if (res1 == '-' or res2 == '-') or res1 == res2:
         compstr += str(0)
    elif res1 != res2:
        compstr += str(1)
    else:
        pass

mean = calc_mean(compstr)

zlist = []
for s,e in get_indices(compstr):
    try:
        zlist.append(calc_zscore(compstr, s, e, window_size, mean))
    except(ValueError,IndexError):
        pass

#print zlist
pylab.plot([z for z in zlist])
pylab.show()
