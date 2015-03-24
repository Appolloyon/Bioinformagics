#!/usr/bin/env python

import sys
import re

treefile = sys.argv[1]
namefiles = sys.argv[2:]

redict = {}
for nfile in namefiles:
    suffix = nfile.split('.')[0]
    with open(nfile,'U') as i:
        for line in i:
            if line.startswith('>'):
                line = line.strip('>').strip('\n')
                rstring = line + '_' + str(suffix)
                redict[line] = rstring
#print redict

outfile = treefile
with open(treefile,'U') as i2:
    wstring = ''
    for line in i2:
        line = line.strip('\n')
        wstring += line
#print wstring

for k,v in redict.iteritems():
    if re.search(k,wstring):
        #print k
        #print v
        wstring = re.sub(k,v,wstring)

with open(outfile,'w') as o:
    o.write(wstring + '\n')
