#!/usr/bin/env python

"""
Changelog
---------
Author: Christen Klinger
Last Updated: November 12, 2014
"""

import re
import argparse

parser = argparse.ArgumentParser(
    description = """Writes csv file combining HMMer and Pfam output""",
    epilog = """This program assumes already parsed data for HMMer and
    Pfam output (as csv files using pfam_parse.py and hmm_parse.py).
    It will extract the information from each accession and write out
    all relevant pieces on each line before moving to a new line.""")
parser.add_argument('-m', '--hmmer', help='HMMer result file')
parser.add_argument('-p', '--pfam', help='Pfam result file')
args = parser.parse_args()

def ExtractAccession(QueryString): #removes just the accession from the hit column
	SearchStr1='\Agi.+'
	SearchStr2='\Ajgi.+'
	SearchStr3='\AsymbB.+'
	SearchStr4='\AContig.+'
	SearchStr5='\ATTHERM.+'
	SearchStr6='\AIMG.+'
	SearchStr7='\Atr.+'
	SearchStr8='\Aprei.+'
	SearchStr9='\Apult.+'
	SearchStr10='\Acrei.+'

	if re.search(SearchStr1, QueryString):
		try:
			StringList1 = QueryString.split('|')
			#print StringList1 #uncomment for debugging
			return StringList1[3]
		except AttributeError:
			return QueryString
	elif re.search(SearchStr2, QueryString):
		try:
			StringList2 = QueryString.split('|')
			#print StringList2
			return StringList2[2]
		except AttributeError:
			return QueryString
	elif re.search(SearchStr3, QueryString) or re.search(SearchStr4, QueryString):
		try:
			StringList3 = QueryString.split('|')
			#print StringList3
			return StringList3[0]
		except AttributeError:
			return QueryString
	elif re.search(SearchStr5, QueryString) or re.search(SearchStr6, QueryString):
		try:
			ResultStr='(\w+_\d+)#\w+'
			ResultSearch = re.search(ResultStr, QueryString)
			Result = ResultSearch.group(1)
			return Result
		except AttributeError:
			return QueryString
	elif re.search(SearchStr7, QueryString) or re.search(SearchStr8, QueryString)\
	or re.search(SearchStr9, QueryString) or re.search(SearchStr10, QueryString):
		try:
			StringList4 = QueryString.split('|')
			#print StringList4
			return StringList4[1]
		except:
			return QueryString
	else:
		return QueryString

def nonblank_lines(f):
	for l in f:
		line = l.strip('\n')
		if line:
			yield line

HFile = args.hmmer
PFile = args.pfam

with open(HFile, 'r') as f1:
	HList=[]
	for line in nonblank_lines(f1):
#		print line
		Hlist = line.split(',')
#		print Hlist
		try:
			HAcc = ExtractAccession(Hlist[0])
			HEvalue = float(Hlist[1])
		except(IndexError):
			pass

		HList.append([HAcc,HEvalue])
#	print HList

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
			PAcc = ExtractAccession(current_list2[0])
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
		if ExtractAccession(current_list2[0])!=ExtractAccession(prev_list2[0]):
			PDict[PAcc]=[]
			PDict[PAcc] += [AStart,AEnd,EStart,EEnd,PfamID,Name,Type,PEvalue]
		else:
			PDict[PAcc] += [AStart,AEnd,EStart,EEnd,PfamID,Name,Type,PEvalue]
		prev_line2 = current_line2
#	print PDict

with open("Out.csv",'w') as O:
	for HA,HE in HList:
		O.write("%s,%s," % (HA,HE))
		try:
			for v in PDict.get(HA):
				O.write("%s," % (v))
		except(TypeError):
			pass
		O.write('\n')


