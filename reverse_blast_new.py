#!/usr/bin/env python

import os
import re
import math
import argparse

parser = argparse.ArgumentParser(
    description = "Combines forward and reverse BLAST searches",
    epilog = """This program takes tabular BLAST output for forward and
    reverse BLAST searches with the same query sets, and makes csv output
    files for each query/db combination of potential hits""")
parser.add_argument('-f', '--forwarddir', help='directory with forward BLAST files')
parser.add_argument('-r', '--reversedir', help='directory with reverse BLAST files')
parser.add_argument('-e', '--evalue', default=0.05, help='evalue cutoff to display hits')
parser.add_argument('-o', '--out', help='name for outfile')
parser.add_argument('-d1', '--diff1', default=2, help='first evalue cutoff diff')
parser.add_argument('-d2', '--diff2', default=2, help='second evalue cutoff diff')
args = parser.parse_args()

curdir = os.getcwd()
forward_dir = os.path.join(curdir,args.forwarddir)
reverse_dir = os.path.join(curdir,args.reversedir)
ffiles = [f for f in os.listdir(forward_dir) if \
    os.path.isfile(os.path.join(forward_dir,f)) and f.endswith('.txt')]
rfiles = [f for f in os.listdir(reverse_dir) if \
    os.path.isfile(os.path.join(reverse_dir,f)) and f.endswith('.txt')]

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
            qacc = curlist[0]
            sacc = curlist[1]
            evalue = float(curlist[3])
            if qacc not in bdict.keys():
                bdict[qacc] = []
                bdict[qacc].append([sacc,evalue])
            else:
                bdict[qacc].append([sacc,evalue])
        prevline = line

fdict = {}
for ffile in ffiles:
    with open(os.path.join(forward_dir,ffile),'U') as ff:
        parseblast(ff,fdict)

with open(args.out,'w') as o:
    o.write("query,forward hit number,forward hit,forward evalue,reverse evalue,")
    o.write("result status,evalue diff first,evalue diff last")
    o.write(2 * '\n')
    for query in sorted(fdict): # go by queries
        for rfile in rfiles: #iterate over every file in rfiles
            if re.search(str(query),str(rfile)):
                with open(os.path.join(reverse_dir,rfile),'U') as rf:
                    rdict = {}
                    parseblast(rf,rdict)
                    fwd_hit_num = 0

                    for fhit,feval in fdict[query]:
                        for subj in rdict:
                            if fhit == subj and float(feval) <= float(args.evalue): #we have the record for the fBLAST entry
                                rev_hit_num = 0 #keep track of which rBLAST hit this is
                                first_hit_match = False
                                result_status = 'negative'
                                evalues = []
                                num_hits = len(rdict[subj])
                                result_status_determined = False
                                raw_rev_eval_first_match = None

                                for rhit,reval in rdict[subj]: #now iterate over the list of rBLAST hits
                                    if reval == 0.0:
                                        new_reval = 1e-300
                                    else:
                                        new_reval = reval
                                    if float(new_reval) <= args.evalue:
                                        match = False
                                        if rhit == query:
                                            match = True
                                        if rev_hit_num == 0 and match: #first hit is a match
                                            first_hit_match = True
                                            raw_rev_eval_first_match = reval

                                        if first_hit_match and match:
                                            if rev_hit_num == (num_hits - 1): #we only found positive hits
                                                result_status_determined = True
                                                if rev_hit_num == 0:
                                                    eval_diff_first = 'NA'
                                                else:
                                                    eval_diff_first = abs(math.log(float(evalues[0]),10)\
                                                        - math.log(float(new_reval),10))
                                                eval_diff_last = 'NA'

                                                result_status = 'positive'
                                                o.write("%s,%s,%s,%s,%s,%s,%s,%s" %
                                                    (query,fwd_hit_num,fhit,feval,raw_rev_eval_first_match,\
                                                    result_status,eval_diff_first,eval_diff_last))
                                                break
                                            else:
                                                pass
                                        elif first_hit_match and not match:
                                            result_status_determined = True
                                            eval_diff_first = abs(math.log(float(evalues[0]),10)\
                                                - math.log(float(new_reval),10))
                                            eval_diff_last = abs(math.log(float(evalues[(len(evalues) - 1)]),10)\
                                                - math.log(float(new_reval),10))
                                            if eval_diff_first >= args.diff1 and eval_diff_last >= args.diff2:
                                                result_status = 'positive'
                                            else:
                                                result_status = 'uncertain'
                                            o.write("%s,%s,%s,%s,%s,%s,%s,%s" %
                                                (query,fwd_hit_num,fhit,feval,raw_rev_eval_first_match,\
                                                result_status,eval_diff_first,eval_diff_last))
                                            break
                                        elif not first_hit_match and match:
                                            result_status_determined = True
                                            result_status = 'unlikely'
                                            o.write("%s,%s,%s,%s,%s,%s,%s,%s" %
                                                (query,fwd_hit_num,fhit,feval,reval,result_status,'NA','NA'))
                                            break
                                        else:
                                            break
                                    rev_hit_num += 1
                                    evalues.append(new_reval)

                                if not result_status_determined:
                                    result_status = 'NEGATIVE'
                                    o.write("%s,%s,%s,%s,%s,%s,%s,%s" %
                                        (query,fwd_hit_num,fhit,feval,'NA',result_status,'NA','NA'))
                                o.write('\n')
                        fwd_hit_num += 1
                o.write('\n')

