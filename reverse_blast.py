#!/usr/bin/env python

import os
import argparse

parser = argparse.ArgumentParser(
    description = "Combines forward and reverse BLAST searches",
    epilog = """This program takes tabular BLAST output for forward and
    reverse BLAST searches with the same query sets, and makes csv output
    files for each query/db combination of potential hits""")
parser.add_argument('-f', '--forwarddir', help='directory with forward BLAST files')
parser.add_argument('-r', '--reversedir', help='directory with reverse BLAST files')
parser.add_argument('-c', '--cutoff', help='cutoff for subsequent hits in rBLAST')
parser.add_argument('-n', '--numhits', help='max number of hits to show')
parser.add_argument('-e', '--evalue', default=0.05, help='evalue cutoff to display hits')
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

def parseblast(bfile,bdict):
    prevline = ''
    for line in bfile:
        curlist = line.strip('\n').split('\t')
        try:
            prevlist = prevline.strip('\n').split('\t')
        except:
            pass
        if curlist[0] == prevlist[0] and curlist[1] == prevlist[1]:
            pass
        else:
            if curlist[0] not in bdict.keys():
                bdict[curlist[0]] = []
                bdict[curlist[0]].append([curlist[1],curlist[2],curlist[3]])
            else:
                bdict[curlist[0]].append([curlist[1],curlist[2],curlist[3]])
        prevline = line

fdict = {}
for ffile in ffiles:
    with open(os.path.join(forward_dir,ffile),'U') as ff:
        parseblast(ff,fdict)

#rdict = {}
#for rfile in rfiles:
#    with open(os.path.join(reverse_dir,rfile),'U') as rf:
#        parseblast(rf,rdict)

for query in fdict:
    lout = query + '_full_rBLAST.csv'
    rout = query + '_RBH_rBLAST.csv'
    #sout = query + '_sig_rBLAST.csv'
    with open(lout,'w') as lo, open(rout,'w') as ro: #open(sout,'w') as so:
        for rfile in rfiles:
            with open(os.path.join(reverse_dir,rfile),'U') as rf:
                rdict = {}
                parseblast(rf,rdict)
                qcounter = 1
                for fhit,feval,ftitle in fdict[query]:
                    for subj in rdict:
                        if fhit == subj and float(feval) <= float(args.evalue):
                            scounter = 1
                            lo.write("%s,%s,%s," % (query,fhit,feval))
                            for rhit,reval,rtitle in rdict[subj]:
                                if scounter < int(args.numhits) + 1:
                                    if float(reval) <= float(args.evalue):
                                        lo.write("%s,%s," % (rhit,reval))
                                        if rhit == query and scounter == 1:
                                            ro.write("%s,%s,%s,%s,%s,%s," % (qcounter,query,scounter,fhit,feval,reval))
                                            ro.write('confirmed hit,')
                                            ro.write("%s" % (rtitle))
                                            ro.write('\n')
                                        elif rhit == query and scounter != 1:
                                            #print 'reval: ' + reval
                                            #print 'comparison: ' + rdict[subj][0][1]
                                            #print 'diff is: ' + str(abs(float(reval) - float(rdict[subj][0][1])))
                                            if abs(float(reval) - float(rdict[subj][0][1])) > float(args.cutoff):
                                                ro.write("%s,%s,%s,%s,%s,%s," % (qcounter,query,scounter,fhit,feval,reval))
                                                ro.write('tenuous hit,')
                                                ro.write("%s" % (rtitle))
                                                ro.write('\n')
                                    scounter += 1
                            lo.write('\n')
                            qcounter += 1
                lo.write('\n')
                ro.write('\n')
#for query in fdict:
#    for fhit,feval,ftitle in fdict[query]:
#        for rhit,qacc,reval,rtitle in rlist:
#            if query == qacc and rhit == fhit:
#                print query + ' ' + fhit + ' ' + feval + ' ' + reval + ' '

