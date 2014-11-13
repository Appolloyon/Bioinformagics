#!/usr/bin/env python

"""
Changelog
---------
Author: Christen Klinger
Last Updated: November 13, 2014
"""

import os
import re
import sys
import argparse

parser = argparse.ArgumentParser(
    description = """Obtains just the accessions from tabular output.""",
    epilog = """This program takes tabular input and retrieves just the
    accessions from each line. Options allow users to skip header lines
    and specify which column to use for getting the accessions.""")
parser.add_argument('-c', '--column', type=int,
                    help='specify column with accession')
parser.add_argument('-d', '--header', type=int, default=0,
                    help='specify number of header lines to skip')
parser.add_argument('-o', '--output', type=int, default=4,
                    help='number of infile name sections to keep')
parser.add_argument('infiles', nargs='+', help='list of infiles')
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


col_num = args.column
num_skips = args.header
out_skips = args.output
file_list = args.infiles

for infile in file_list:
	sys.stderr.write("Processing file %s\n" % (infile))

file_num=0

for infile in file_list:
    infile_info = os.stat(infile)
    infile_size = infile_info.st_size
    if infile_size != 0:
        outlist = (infile.split('_'))[0:out_skips]
        outname = ''
        for e in outlist:
            outname += (e + '_')
        outfile = outname + "Acc.txt"

        with open(infile, 'U') as i, open(outfile, 'w') as o:
            linenum = 1
            for line in i:
                if linenum > num_skips:
                    line=line.strip('\n')
                    element_list=line.split()

                    outacc = ExtractAccession(element_list[(col_num - 1)])
                    #print OutAcc

                    outstring = "%s" % (outacc)
                    o.write(outstring + '\n')
                linenum += 1
            file_num += 1

sys.stderr.write("Finished processing %s files\n" % (file_num))

"""
Changelog:
28/10/14: Remove .csv extension (expected in input file)
29/10/14: Strips off any file extension, not specified any longer
          Now uses 'with open' statements, instead of opening and closing manually
"""

