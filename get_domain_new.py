#!/usr/bin/env python

"""
Changelog
---------
Author: Christen Klinger
Last updated: January 14, 2015
"""

import argparse
from functions import nonblank_lines,split_input

parser = argparse.ArgumentParser(
    description = """Gets domain sequences from specified domains""",
    epilog = """This program requires two input files, a csv file with the
    domains desired and a .fa file with the corresponding sequences to pull
    domains out of. Domains will be named by the input accession, domain name,
    and by the start and end coordinates of the domain in question""")
parser.add_argument('-d', '--domain', help='domain file')
parser.add_argument('-s', '--sequence', help='sequence file')
args = parser.parse_args()

dfile = args.domain
sfile = args.sequence
ofile = sfile.strip('.fa') + "_doms.fa"

with open(sfile, 'U') as i1:
    seqdict = {}
    for line in nonblank_lines(i1):
        if line.startswith('>'):
            line = line.strip('>').strip('\n')
            ID = line
            seqdict[ID] = ''
        else:
            line = line.strip('\n')
            seqdict[ID] += line

with open(dfile, 'U') as i2:
    domlist = []
    for line in i2:
        line = line.strip('\n').split(',')
        try:
            acc = line[0]
            start = line[3]
            end = line[4]
            domname = line[6]
            domlist.append([acc,start,end,domname])
        except(IndexError):
            pass

with open(ofile, 'w') as o:
    for A,S,E,DN in domlist:
        if A in seqdict.keys():
            dom = seqdict[A][int(S)-1:int(E)]
            o.write('>' + A + '-' + DN + '\n')
            input_chunks = split_input(dom, 80)
            for chunk in input_chunks:
                o.write(chunk + '\n')
