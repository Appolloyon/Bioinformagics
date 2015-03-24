#!/usr/bin/env python

import sys

InFile = sys.argv[1]

with open(InFile, 'r') as f:
	seqdict={}
	for curline in f:
		if curline.startswith(">"):
			curline=curline.strip(">").strip('\n')
			ID = curline
			seqdict[ID] = ''
		else:
			curline=curline.strip('\n')
			seqdict[ID] += curline
#print seqdict

for k in seqdict:
	count = 0
	for v in seqdict.get(k):
		count += len(v)
	print k, count
