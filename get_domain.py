#!/usr/bin/env python

import re
import os

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

def split_input(string, chunk_size):
	num_chunks = len(string)/chunk_size
	if (len(string) % chunk_size != 0):
		num_chunks += 1
	output = []
	for i in range (0, num_chunks):
		output.append(string[chunk_size*i:chunk_size*(i+1)])
	return output

def nonblank_lines(f):
	for l in f:
		line = l.strip('\n')
		if line:
			yield line

Seq_Dir = (os.getcwd()+"/Sequences")
Dom_Dir = (os.getcwd()+"/Domains")

FileList_Seqs = [f for f in os.listdir(Seq_Dir) if \
os.path.isfile(os.path.join(Seq_Dir,f)) and f.endswith(".fa")]

FileList_Doms = [f for f in os.listdir(Dom_Dir) if \
os.path.isfile(os.path.join(Dom_Dir,f)) and f.endswith(".csv")]

OutDir = (os.getcwd()+"/DomSeqs")
if not os.path.exists(OutDir):
	os.makedirs(OutDir)

for File1 in FileList_Seqs:
	for File2 in FileList_Doms:
		pattern1 = (re.search('(\w+)_(\w+)(.+)',File1).group(1))
		if re.search(pattern1,File2):
			pattern2 = (re.search('(\w+)_(\w+)(.+)',File2).group(2))
			Out=pattern1 + "_" + pattern2 + ".fa"
			with open(os.path.join(Seq_Dir,File1), 'U') as f1:
				seqdict={}
				for line in nonblank_lines(f1):
					if line.startswith(">"):
						line = line.strip(">").strip('\n')
						ID = ExtractAccession(line)
						seqdict[ID] = ''
					else:
						line = line.strip('\n')
						seqdict[ID] += line
			with open(os.path.join(Dom_Dir,File2), 'U') as f2:
				DomList = []
                for line in f2:
                    print line
                    line = line.strip('\n').split(',')
                    Acc = ExtractAccession(line[0])
                    Start = line[3]
                    End = line[4]
                    DomList.append([Acc,Start,End])

            with open((os.path.join(OutDir,Out)),'w') as o:
                for A,S,E in DomList:
					try:
						dom = seqdict[A][int(S)-6:int(E)+5]
					except(IndexError):
						dom = seqdict[A][int(S)-1:int(E)]
					o.write(">" + A + '\n')
					input_chunks=split_input(dom, 80)
					for chunk in input_chunks:
						o.write(chunk + '\n')
