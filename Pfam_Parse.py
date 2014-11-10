#!/usr/bin/env python

Usage="""
Pfam_Parse.py
Reads in a Pfamscan output file and returns a csv file with the domain envelopes,
Pfam IDs, Names, and E value of all domains.

usage: Pfam_Parse.py 'files to parse'
"""

import os
import re
import sys

if len(sys.argv) < 2:
	print Usage
	sys.exit(1) #exits without traceback if no args given

else: 
	FileList = sys.argv[1:] #list of args to loop over
	for InFileName in FileList:
		sys.stderr.write("Processing file %s\n" % (InFileName))

PathList = os.getcwd() #not hardcoded for particular directory

PathString='.+/(\w+)\Z' 
PathElement = re.search(PathString, PathList) 

PathName = PathElement.group(1) #returns the last folder name
OutDir = (PathList + '/PfamScanSorted')

if not os.path.exists(OutDir):
	os.makedirs(OutDir)

MasterOutName = PathName + '_Sorted.csv'
MasterOut = open(os.path.join(OutDir, MasterOutName), 'w')

FileNum=0

for InFileName in FileList:
	print InFileName
	InFileInfo = os.stat(InFileName)
	InFileSize = InFileInfo.st_size
	if InFileSize != 0: #don't bother reading empty files

		with open (InFileName, 'U') as InFile:
			LineNum = 0
			for Line in InFile:
				Line=Line.strip('\n')
#				print Line
				if not Line.startswith("#"):
					#print Line
					try:
						ElementList=Line.split()
#						print ElementList
					
						Query = ElementList[0]
						AlignStart = int(ElementList[1])
						AlignEnd = int(ElementList[2])
						EnvStart = int(ElementList[3])
						EnvEnd = int(ElementList[4])
						PfamID = ElementList[5]
						Name = ElementList[6]
						Type = ElementList[7]
						Evalue = float(ElementList[12])

						OutString = "%s,%d,%d,%d,%d,%s,%s,%s,%s" % (Query,AlignStart,\
						AlignEnd,EnvStart,EnvEnd,PfamID,Name,Type,Evalue)

						MasterOut.write(OutString)
						MasterOut.write('\n')
					except(IndexError):
						pass

				LineNum += 1

		FileNum += 1
		MasterOut.write('\n')
	
sys.stderr.write("Finished processing %s files\n" % (FileNum))

MasterOut.close()