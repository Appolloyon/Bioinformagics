#!/usr/bin/env python

import re
import sys

infile = sys.argv[1]

def nonblank_lines(f):
    for l in f:
        line = l.strip('\n')
        if line:
            yield line

def split_input(string, chunk_size):
    num_chunks = len(string)/chunk_size
    if (len(string) % chunk_size != 0):
        num_chunks += 1
    output = []
    for i in range(0, num_chunks):
        output.append(string[chunk_size*i:chunk_size*(i+1)])
    return output

with open(infile,'U') as i:
    seqdict = {}
    for line in nonblank_lines(i):
        if line.startswith('>'):
            line = line.strip('>').strip('\n')
            ID = line
            seqdict[ID] = ''
        else:
            line = line.strip('\n')
            seqdict[ID] += line

outfile = infile.rstrip('.fa')
outfile = outfile + '_reduced.fa'
with open(outfile,'w') as o:
    for k in seqdict.keys():
        if re.search('Toxoplasma',k) or re.search('Plasmodium',k) or \
        re.search('Babesia',k) or re.search('Theileria',k) or \
        re.search('Cryptosporidium',k):
            print 'removing sequence: ' + k
            print '\n'
        else:
            o.write('>' + k + '\n')
            input_chunks = split_input(seqdict[k],60)
            for chunk in input_chunks:
                o.write(chunk + '\n')
