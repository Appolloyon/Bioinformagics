#!/usr/bin/env python

import itertools
import sys
import os

infile = sys.argv[1]
outfile = os.path.splitext(infile)[0]
outfile = outfile + "_uniq.csv"

with open(infile, 'U') as f, open(outfile, 'w') as o:
    L1 = []
    for line in f:
        llist = line.split(',')
        Qacc = llist[0]
        Sacc = llist[1]
        Eval = llist[2]
        L1.append([Qacc, Sacc, Eval])
    #print L1

