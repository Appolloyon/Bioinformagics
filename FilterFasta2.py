#!/usr/bin/env python

import os
import sys
import re

InFileList = sys.argv[1:]

def read_FASTA_iteration(filename):
	sequences = []
	descr = None
	with open(filename, 'r') as file:
		for line in file:
			if line[0] == '>':
				if descr:
					sequences.append((descr, seq))
				descr = line[1:-1].split('|')
				print descr
				seq = ''
			else:
				seq += line[:-1]
		sequences.append((descr, seq))
	print sequences
	return sequences

def confirm_header(line):
	SearchStr = '\A>prei|\w+_\d+'
	if re.search (SearchStr, line):
		return True

for filename in InFileList:
	read_FASTA_iteration(filename)
	print sequences
	outfilename = filename + "_output.fa"
	with open(outfilename, 'w') as outfile:
		for element in sequences:
			outfile.write(element + "\n")
