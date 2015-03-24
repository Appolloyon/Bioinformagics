#!/usr/bin/env python

import sys

infile = sys.argv[1]
outfile = infile
with open(infile, 'U') as i:
    flist = []
    for line in i:
        llist = line.strip('\n').split('\t')
        elist = llist[1].split('#')
        query = llist[0]
        sacc = elist[0]
        evalue = llist[2]
        flist.append([query, sacc, evalue])

with open(outfile, 'w') as o:
    for q, s, e in flist:
        o.write("%s\t%s\t%s" % (q, s, e))
        o.write('\n')


