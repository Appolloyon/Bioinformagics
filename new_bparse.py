#!/usr/bin/env python

"""
This program parses tabular BLAST output into a more usable form. Assuming
BLAST input of the form "qacc sacc evalue" this program will return a csv
file with just the accessions from each of qacc and sacc, along with the
evalue, however, duplicate sacc lines will be ignored and only the best e
value will be registered for each hit
"""

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

FileList = sys.argv[1:] #list of args to loop over
for InFileName in FileList:
	sys.stderr.write("Processing file %s\n" % (InFileName))

PathList = os.getcwd() #not hardcoded for particular directory
PathString='.+/(\w+)\Z'
PathElement = re.search(PathString, PathList)
PathName = PathElement.group(1) #returns the last folder name
OutDir = (PathList + '/Sorted')

if not os.path.exists(OutDir):
	os.makedirs(OutDir)

MasterOut = PathName + '_Sorted.csv'
#MasterOut = open(os.path.join(OutDir, MasterOutName), 'w')

FileNum=0

with open(os.path.join(OutDir,MasterOut), 'w') as o:
	for File in FileList:
		with open(File, 'r') as f:
			FList=[]
			prev_line=''
			for current_line in f:
#			print "Current:" + current_line1
#			print "Previous:" + prev_line1
				current_list = current_line.strip('\n').split('\t')
				try:
					prev_list = prev_line.strip('\n').split('\t')
				except(ValueError, TypeError, NameError):
					pass
				if (ExtractAccession(current_list[0])==ExtractAccession(prev_list[0]) \
				and ExtractAccession(current_list[1])==ExtractAccession(prev_list[1])):
					pass
				else:
					FAcc = ExtractAccession(current_list[0])
					FHit = ExtractAccession(current_list[1])
					FEvalue = float(current_list[2])

					o.write("%s,%s,%s" %(FAcc,FHit,FEvalue) + "\n")

				prev_line = current_line
