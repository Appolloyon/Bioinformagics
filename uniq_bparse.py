#!/usr/bin/env python

Usage = """
uniq_bparse.py

This program takes already parsed BLAST data in csv format with Qacc, Sacc, Eval
on each line and returns a csv file of identical format sorted for increasing
E value and only unique elements. This is to say that only the top hit for each
potential Sacc is reported, and therefore it is unique

usage: uniq_bparse.py {files to parse}

Created: October 29, 2014
Author: Christen M Klinger
Last Updated: October 29, 2014
"""

import sys
import os
from operator import itemgetter

def comp_hits(pair):
    hit1 = pair[0]
    hit2 = pair[1]
    if hit1[1] == hit2[1]:
        if hit1[2] < hit2[2]:
            return hit1
        else:
            return hit2

infiles = sys.argv[1:]
for infile in infiles:
    outfile = os.path.splitext(infile)[0]
    outfile = outfile + "_uniq.csv"

    with open(infile, 'U') as f, open(outfile, 'w') as o:
        L1 = []
        for line in f:
            llist = line.split(',')
            Qacc = llist[0]
            Sacc = llist[1]
            Eval = float(llist[2])
            L1.append([Qacc, Sacc, Eval])

        L2 = sorted(L1, key = itemgetter(2))
        test = set()
        L3 = []
        for x in L2:
            if x[1] in test:
                pass
            else:
                test.add(x[1])
                L3.append(x)
        #print test
        #print L3

        for el in L3:
            o.write(str(el[0]) + "," + str(el[1]) + "," + str(el[2]))
            o.write("\n")
