#!/usr/bin/env python

from Bio import SeqIO
import sys
import re
import os

def DetermineSplit(QueryString):
	if re.search('|', QueryString):
		return '|'
	else:
		return ' '

def GetFastaFile(Input):
	onlyfiles = [ f for f in os.listdir(Input) ]
	for f in onlyfiles:
		if re.search("_Prot.fa", f):
			fasta_file_name = f
			return fasta_file_name

FileList = sys.argv[1:] #list of args to loop over

PathList2 = "/Users/chrisklinger/Documents/Genomes_new_2014"

for InFileName in FileList:
	sys.stderr.write("Processing file %s\n" % (InFileName))
	SearchStr = '(\w+)_(\w+.\w+)'
	GenomeIdentity = re.search(SearchStr, InFileName)
	GenomeTag = GenomeIdentity.group(1)
#	print GenomeTag
	GenomeDir = (PathList2 + '/' + GenomeTag +'/')
#	print GenomeDir
	OutName = GenomeTag + "_Seqs.fa"

	wanted = set()

	with open(InFileName,'r') as f:
		for line in f:
			line = line.strip('\n').split(',')
			if line[0] != "":
				wanted.add(line[0])
		#print wanted
	
		for element in wanted:
			re.sub('\r', '', element)
			#print wanted

		fasta_file_name = GetFastaFile(GenomeDir)
		print fasta_file_name
		fasta_file = GenomeDir + fasta_file_name
		fasta_sequences = SeqIO.parse(open(fasta_file),'fasta')

		with open(OutName,'w') as o:

			for seq in fasta_sequences:
				new_header = seq.description.replace(" ", "|").replace("\t", "|")
				IdList = new_header.split(DetermineSplit(seq.description))
				#print IdList
				for element in IdList:
					#print element
					if element in wanted:
						SeqIO.write([seq], o, "fasta")