#!/usr/bin/env python

Usage="""
New_Get_Acc_List.py
Intended to be used in conjunction with pyGetFasta.py, this program
will take any file with accessions in the X position of each line
and return a separate file with just the accessions, one per line.

Usage: New_Get_Acc_List.py '-X' '-Y' 'files to parse'

where -X is the column number with accessions, and -Y is the number
of lines to skip (header; default should be 0)

Author: Christen Klinger
Last Modified: October 28, 2014
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

def get_col_num(ColumnNum):
	ColNum = int((re.search('(-)(.+)', ColumnNum)).group(2))
	return ColNum


if len(sys.argv) < 2:
	print Usage
	sys.exit(1) #exits without traceback if no args given
else:
    ColumnNum = sys.argv[1]
    NumSkips = get_col_num(sys.argv[2])
    FileList = sys.argv[3:] #list of args to loop over

for InFileName in FileList:
	sys.stderr.write("Processing file %s\n" % (InFileName))

FileNum=0

for InFileName in FileList:
	InFileInfo = os.stat(InFileName)
	InFileSize = InFileInfo.st_size
	if InFileSize != 0: #don't bother reading empty files

		OutName = os.path.splitext(InFileName)[0]
		OutName = OutName + "_Acc.txt"

        with open(InFileName, 'U') as I, open(OutName, 'w') as o:
            LineNum = 1
            for Line in I:
                if LineNum > NumSkips:
                    Line=Line.strip('\n')
                    ElementList=Line.split()

                    col_num = get_col_num(ColumnNum)
                    OutAcc = ExtractAccession(ElementList[(col_num - 1)])
                    #print OutAcc

                    OutString = "%s" % (OutAcc)
                    o.write(OutString)
                    o.write('\n')
                LineNum += 1
            FileNum += 1

sys.stderr.write("Finished processing %s files\n" % (FileNum))

"""
Changelog:
28/10/14: Remove .csv extension (expected in input file)
29/10/14: Strips off any file extension, not specified any longer
          Now uses 'with open' statements, instead of opening and closing manually
"""

