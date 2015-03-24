#!/usr/bin/env python

import sys

files = sys.argv[1:]
out = 'GTP_sort.csv'

def snare_fam(llist):
    lowest_name = ''
    lowest_evalue = 1
    for name,evalue in llist:
        if evalue < lowest_evalue:
            lowest_name = name
            lowest_evalue = evalue
    return (lowest_name,lowest_evalue)


sdict = {}
for sf in files:
    name = sf.strip('\n').split('_')[0]
    with open(sf,'U') as f:
        linenum = 0
        for l in f:
            if linenum > 2:
                l = l.strip('\n')
                elist = l.split()

                acc = elist[0]
                evalue = float(elist[4])

                if acc not in sdict:
                    sdict[acc] = []
                    sdict[acc].append([name,evalue])
                else:
                    sdict[acc].append([name,evalue])
            linenum += 1

#print sdict

with open(out,'w') as o:
    for acc in sdict:
        wname,weval = snare_fam(sdict[acc])
        o.write("%s,%s,%s" % (wname,acc,weval))
        o.write('\n')

