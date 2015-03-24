#!/usr/bin/env python

"""
Changelog
---------
Author: Christen Klinger
Last Updated: November 12, 2014
"""

import argparse
from functions import extractacc, nonblank_lines

parser = argparse.ArgumentParser(
    description = """Writes csv file combining HMMer and Pfam output""",
    epilog = """This program assumes already parsed data for HMMer and
    Pfam output (as csv files using pfam_parse.py and hmm_parse.py).
    It will extract the information from each accession and write out
    all relevant pieces on each line before moving to a new line.""")
group = parser.add_mutually_exclusive_group()
group.add_argument('-m', '--hmmer', help='HMMer result file')
group.add_argument('-b', '--blast', help='BLAST result file')
parser.add_argument('-p', '--pfam', help='Pfam result file')
args = parser.parse_args()

if args.hmmer:
    HFile = args.hmmer
elif args.blast:
    BFile = args.blast
PFile = args.pfam

if args.hmmer:
    with open(HFile, 'r') as f1:
        HList=[]
        for line in nonblank_lines(f1):
            #print line
            Hlist = line.split(',')
            #print Hlist
            try:
                HAcc = extractacc(Hlist[0])
                HEvalue = float(Hlist[1])
            except(IndexError):
                pass
            HList.append([HAcc,HEvalue])
            #print HList
elif args.blast:
    with open(BFile, 'r') as f3:
        BList=[]
        for line in nonblank_lines(f3):
            Blist = line.split(',')
            try:
                QAcc = extractacc(Blist[0])
                BAcc = extractacc(Blist[1])
                BEvalue = float(Blist[2])
            except(IndexError):
                pass
            BList.append([QAcc,BAcc,BEvalue])

with open(PFile, 'r') as f2:
	PDict={}
#	AccList=[]
	prev_line2=''
	for current_line2 in nonblank_lines(f2):
#		print "Current:" + current_line2
#		print "Previous:" + prev_line2
		current_list2 = current_line2.split(',')
		try:
			prev_list2 = prev_line2.split(',')
		except(ValueError, TypeError, NameError):
			pass
		try:
			PAcc = extractacc(current_list2[0])
			AStart = float(current_list2[1])
			AEnd = float(current_list2[2])
			EStart = float(current_list2[3])
			EEnd = float(current_list2[4])
			PfamID = current_list2[5]
			Name = current_list2[6]
			Type = current_list2[7]
			PEvalue = float(current_list2[8])
		except(IndexError):
			pass
		if extractacc(current_list2[0])!=extractacc(prev_list2[0]):
			PDict[PAcc]=[]
			PDict[PAcc] += [AStart,AEnd,EStart,EEnd,PfamID,Name,Type,PEvalue]
		else:
			PDict[PAcc] += [AStart,AEnd,EStart,EEnd,PfamID,Name,Type,PEvalue]
		prev_line2 = current_line2
#print PDict

with open("Out.csv",'w') as O:
    if args.hmmer:
        for HA,HE in HList:
            O.write("%s,%s," % (HA,HE))
            try:
                for v in PDict.get(HA):
                    O.write("%s," % (v))
            except(TypeError):
                pass
            O.write('\n')
    elif args.blast:
        for QA,BA,BE in BList:
            O.write("%s,%s,%s," % (QA,BA,BE))
            try:
                for v in PDict.get(BA):
                    O.write("%s," % (v))
            except(TypeError):
                pass
            O.write('\n')


