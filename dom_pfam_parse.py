#!/usr/bin/env python

import re
import os
import os.path
import sys

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

csv_file = sys.argv[1]

with open(csv_file, 'r') as f:
	PDict={}
#	AccList=[]
	prev_line=''
	for current_line in nonblank_lines(f):
#		print "Current:" + current_line
#		print "Previous:" + prev_line
		current_list = current_line.split(',')
		try:
			prev_list = prev_line.split(',')
		except(ValueError, TypeError, NameError):
			pass
		try:
			PAcc = ExtractAccession(current_list[0])
			AStart = float(current_list[1])
			AEnd = float(current_list[2])
			PfamID = current_list[5]
			Name = current_list[6]
			Type = current_list[7]
			PEvalue = float(current_list[8])
		except(IndexError):
			pass
		if ExtractAccession(current_list[0])!=ExtractAccession(prev_list[0]):
			PDict[PAcc]=[]
			PDict[PAcc].append([AStart,AEnd,PfamID,Name,Type,PEvalue])
		else:
			PDict[PAcc].append([AStart,AEnd,PfamID,Name,Type,PEvalue])
		prev_line = current_line
#	print PDict