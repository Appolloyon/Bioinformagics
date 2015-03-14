#!/usr/bin/env python

"""
Changelog
---------
Author: Christen Klinger
Last updated: November 12, 2014
"""

import argparse
from functions import split_input

parser = argparse.ArgumentParser(
    description = """Formats sequence files in FASTA format.""",
    epilog = """This program is intended to ensure proper formatting of
    FASTA sequence files, namely that sequences should not exceed 80
    characters per line. Input files are read in and written to an
    output file with proper formatting.""")
parser.add_argument('infiles', nargs='+', help='list of infiles')
args = parser.parse_args()

for file in args.infiles:
	NameList = file.split('.')
	Basename = NameList[0]
	OutFile = Basename +'_out.fa'
	with open(OutFile, 'w') as o:
		with open(file, 'r') as f:
			for line in f:
				line = line.strip()
				if line[0] == '>':
					o.write(line + '\n')
				else:
					input_chunks=split_input(line, 80)
					for chunk in input_chunks:
						o.write(chunk + '\n')
