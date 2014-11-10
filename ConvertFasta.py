#!/usr/bin/env python

import os
import re
import sys

def split_input(string, chunk_size):
	num_chunks = len(string)/chunk_size
	if (len(string) % chunk_size != 0):
		num_chunks += 1
	output = []
	for i in range (0, num_chunks):
		output.append(string[chunk_size*i:chunk_size*(i+1)])
	return output

InFileList = sys.argv[1:]

for File in InFileList:
	NameList = File.split('.')
	Basename = NameList[0]
	OutFile = Basename +'_out.fa'
	with open(OutFile, 'w') as o:
		with open(File, 'r') as f:
			for line in f:
				line = line.strip()
				if line[0] == '>':
					o.write(line + '\n')
				else:
					input_chunks=split_input(line, 80)
					for chunk in input_chunks:
						o.write(chunk + '\n')
