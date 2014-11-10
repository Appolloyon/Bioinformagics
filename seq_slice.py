#!/usr/bin/env python 

import sys

in_file = sys.argv[1]
start = int(sys.argv[2])
end = int(sys.argv[3])

with open(in_file, 'r') as f:
	seqdict={}
	for curline in f:
		if curline.startswith(">"):
			curline=curline.strip(">").strip('\n')
			ID = curline
			seqdict[ID] = ''
		else:
			curline=curline.strip('\n')
			seqdict[ID] += curline

for k in seqdict:
	print k
	try:
		print seqdict.get(k)[(start-1):end]
	except(ValueError, IndexError):
		pass