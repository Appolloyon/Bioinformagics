#!/usr/bin/env python

import sys

infile = sys.argv[1]
outfile = sys.argv[2]

with open(infile,'U') as i, open(outfile,'w') as o:
    for line in i:
        if line.startswith('>'):
            line = line.strip('\n')
            llist = line.split('|')
            o.write("%s,%s" % (llist[3],llist[4]))
            o.write('\n')
