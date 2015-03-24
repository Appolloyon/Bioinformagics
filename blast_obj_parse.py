#!/usr/bin/env python

import os
import argparse
from blastrecord import BlastRecord

parser = argparse.ArgumentParser(
    description = "Combines forward and reverse BLAST searches",
    epilog = """This program takes tabular BLAST output for forward and
    reverse BLAST searches with the same query sets, and makes csv output
    files for each query/db combination of potential hits""")
parser.add_argument('-f', '--forwarddir', help='directory with forward BLAST files')
parser.add_argument('-r', '--reversedir', help='directory with reverse BLAST files')
args = parser.parse_args()

curdir = os.getcwd()
forward_dir = os.path.join(curdir,args.forwarddir)
reverse_dir = os.path.join(curdir,args.reversedir)
ffiles = [f for f in os.listdir(forward_dir) if \
    os.path.isfile(os.path.join(forward_dir,f)) and f.endswith('.txt')]
rfiles = [f for f in os.listdir(reverse_dir) if \
    os.path.isfile(os.path.join(reverse_dir,f)) and f.endswith('.txt')]

#print ffiles
#print rfiles

for ffile in ffiles:
    fobj_list = []
    with open(os.path.join(forward_dir,ffile),'U') as ff:
        fprevline = ''
        for fline in ff:
            fcurlist = fline.strip('\n').split('\t')
            try:
                fprevlist = fprevline.strip('\n').split('\t')
            except:
                pass
            if fcurlist[0] == fprevlist[0] and fcurlist[1] == fprevlist[1]:
                pass
            else:
                FAcc = fcurlist[0]
                FHit = fcurlist[1]
                FEvalue = fcurlist[2]
                FTitle = fcurlist[3]

                if len(fobj_list) > 0:
                    for fobj in fobj_list:
                        if fobj.get_ID() == FAcc:
                            fobj.add(FHit, FEvalue, FTitle)
                else:
                    fobj_list.append(BlastRecord(FAcc, FHit, FEvalue, FTitle))
            fprevline = fline

print 'Forward Objects:'
print '\n'
for fobj in fobj_list:
    fobj.print_self()
    print '\n'

for rfile in rfiles:
    robj_list = []
    with open(os.path.join(reverse_dir,rfile),'U') as rf:
        rprevline = ''
        for rline in rf:
            #print 'current line is ' + rline
            #print 'previous line is ' + rprevline
            rcurlist = rline.strip('\n').split('\t')
            try:
                rprevlist = rprevline.strip('\n').split('\t')
            except:
                pass
            if rcurlist[0] == rprevlist[0] and rcurlist[1] == rprevlist[1]:
                pass
            else:
                RAcc = rcurlist[0]
                RHit = rcurlist[1]
                REvalue = rcurlist[2]
                RTitle = rcurlist[3]

                print 'adding values to an object: ' + RAcc + ' ' + RHit + ' ' \
                        + REvalue + ' ' + RTitle

                if len(robj_list) > 0:
                    for robj in robj_list:
                        if robj.get_ID() == RAcc:
                            robj.add(RHit, REvalue, RTitle)
                else:
                    robj_list.append(BlastRecord(RAcc, RHit, REvalue, RTitle))
            rprevline = rline

print 'Reverse Objects:'
print '\n'
for robj in robj_list:
    robj.print_self()
    print '\n'


