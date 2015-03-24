#!/usr/bin/env python

from functions import extractacc
import sys

infile = sys.argv[1]
headerfile = sys.argv[2]
outfile = sys.argv[3]

def parseblast(bfile,bdict):
    prevline = ''
    for line in bfile:
        #print line
        curlist = line.strip('\n').split('\t')
        #print curlist
        try:
            prevlist = prevline.strip('\n').split('\t')
        except:
            pass
        if curlist[0] == prevlist[0] and curlist[1] == prevlist[1]:
            pass
        else:
            if curlist[0] not in bdict.keys():
                #print curlist[1]
                bdict[curlist[0]] = []
                bdict[curlist[0]].append([extractacc(curlist[1]),curlist[2]])
            else:
                bdict[curlist[0]].append([extractacc(curlist[1]),curlist[2]])
        prevline = line

fdict = {}
with open(infile,'U') as i:
    parseblast(i,fdict)

hdict = {}
with open(headerfile,'U') as i2:
    for line in i2:
        line = line.strip('\n')
        llist = line.split(',')
        hdict[llist[0]] = llist[1]

with open(outfile,'w') as o:
    for query in fdict:
        #print query
        counter = 0
        o.write("%s" % (query))
        for fhit,feval in fdict[query]:
            #print "counter is at: " + str(counter)
            #print fhit
            #print feval
            if counter < 20:
                try:
                    fdescr = hdict[fhit]
                except:
                    pass
                o.write(",%s,%s,%s" % (fhit,feval,fdescr))
                o.write('\n')
                counter += 1
        o.write('\n')
