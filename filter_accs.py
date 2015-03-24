#!/usr/bin/env python

import sys

infile = sys.argv[1]
eval_cutoff = float(sys.argv[2])
outfile = infile.strip('.csv')
outfile = outfile + '_FAccs.txt'

with open(infile, 'U') as i:
    acc_dict = {}
    for line in i:
        llist = line.strip('\n').split(',')
        acc = llist[1]
        feval = float(llist[2])
        reval = float(llist[2])
        if acc not in acc_dict.keys() and feval <= eval_cutoff and reval <= eval_cutoff:
            acc_dict[acc] = 1
        elif acc in acc_dict.keys() and feval <= eval_cutoff and reval <= eval_cutoff:
            acc_dict[acc] += 1
        else:
            pass

#for acc in acc_dict:
#    print acc, acc_dict[acc]

with open(outfile, 'w') as o:
    for acc in acc_dict:
        if acc_dict[acc] >= 3:
            o.write(str(acc))
            o.write('\n')
        else:
            pass

