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

infiles = sys.argv[1:]
for infile in infiles:
    outfile = os.path.splitext(infile)[0]  #remove extension only
    outfile = outfile + "_uniq.csv"

    with open(infile, 'U') as f, open(outfile, 'w') as o:
        L1 = []
        for line in f:
            llist = line.split(',')
            Qacc = llist[0]
            Sacc = llist[1]
            Eval = float(llist[2])  #can't sort strings later on
            L1.append([Qacc, Sacc, Eval])

        L2 = sorted(L1, key = itemgetter(2))  #sorts based on E value
        test = set()
        L3 = []
        for x in L2:
            if x[1] in test:  #have we seen a better hit before?
                pass
            else:
                test.add(x[1])  #first time, so add to test
                L3.append(x)  #best hit, so add to L3
        #print test
        #print L3

        for el in L3:
            o.write(str(el[0]) + "," + str(el[1]) + "," + str(el[2]))
            o.write("\n")
