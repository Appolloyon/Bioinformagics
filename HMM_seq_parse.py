#!/usr/bin/env python

Usage="""
HMM_seq_parse.py
reads output HMMer files in tabular format and extracts just the
accession from the hit column and returns the accession and E value
in that order as a csv file. Each file is written as a separate
csv file which can be concatenated as desired.

usage: HMM_seq_parse.py 'files to parse'

Last Updated: October 29, 2014
"""

import os
import re
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
		StringList1 = QueryString.split('|')
		#print StringList1 #uncomment for debugging
		return StringList1[3]
	elif re.search(SearchStr2, QueryString):
		StringList2 = QueryString.split('|')
		#print StringList2
		return StringList2[2]
	elif re.search(SearchStr3, QueryString) or re.search(SearchStr4, QueryString):
		StringList3 = QueryString.split('|')
		#print StringList3
		return StringList3[0]
	elif re.search(SearchStr7, QueryString):
		StringList4 = QueryString.split('|')
		#print StringList4
		return StringList4[1]
	elif re.search(SearchStr5, QueryString) or re.search(SearchStr6, QueryString):
		ResultStr='(\w+_\d+)'
		ResultSearch = re.search(ResultStr, QueryString)
		Result = ResultSearch.group(1)
		return Result
		if None:
			return QueryString
	elif re.search(SearchStr7, QueryString) or re.search(SearchStr8, QueryString)\
	or re.search(SearchStr9, QueryString) or re.search(SearchStr10, QueryString):
		StringList4 = QueryString.split('|')
		#print StringList4
		return StringList4[1]
	else:
		return QueryString

if len(sys.argv) < 2:
	print Usage
	sys.exit(1) #exits without traceback if no args given

else:
	FileList = sys.argv[1:] #list of args to loop over
	for InFileName in FileList:
		sys.stderr.write("Processing file %s\n" % (InFileName))

#PathList = os.getcwd() #not hardcoded for particular directory
#PathString='.+/(\w+)\Z'
#PathElement = re.search(PathString, PathList)
#PathName = PathElement.group(1) #returns the last folder name
#OutDir = (PathList + '/Sequences')
#if not os.path.exists(OutDir):
#	os.makedirs(OutDir)

FileNum=0

for InFileName in FileList:
	InFileInfo = os.stat(InFileName)
	InFileSize = InFileInfo.st_size
	if InFileSize != 0: #don't bother reading empty files
		#GenomeIdent = re.search("(\w+)_(\w+)_(\w+)_.+",InFileName).group(3)
		OutFile = os.path.splitext(InFileName)[0]
        OutFile = OutFile + ".csv"

        with open(InFileName, 'r') as f, open(OutFile, 'w') as o:
			LineNum = 0

			for Line in f:
				if LineNum > 2:
					Line=Line.strip('\n')
					ElementList=Line.split()

					OutAcc = ExtractAccession(ElementList[0])
					#print OutAcc
					Evalue = float(ElementList[4])
					#print Evalue

					OutString = "%s,%s," % (OutAcc,Evalue)

					o.write(OutString)
					o.write('\n')

				LineNum += 1
        FileNum += 1

sys.stderr.write("Finished processing %s files\n" % (FileNum))

"""
Changelog:
29/10/14: Removed separate output dir and made each file a separate output
"""
