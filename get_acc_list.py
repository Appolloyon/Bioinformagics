#!/usr/bin/env python

"""
Changelog
---------
Author: Christen Klinger
Last Updated: November 13, 2014
"""

import os
import sys
import argparse
from functions import extractacc

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
parser.add_argument('-s', '--split', action="store_true",
                    help="true if delimiter is a comma")
parser.add_argument('infiles', nargs='+', help='list of infiles')
args = parser.parse_args()

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
                    try:
                        line=line.strip('\n')
                        if args.split:
                            element_list = line.split(',')
                        else:
                            element_list = line.split()

                        outacc = extractacc(element_list[(col_num - 1)])
                        #print OutAcc

                        outstring = "%s" % (outacc)
                        o.write(outstring + '\n')
                    except:
                        pass
                linenum += 1
            file_num += 1

sys.stderr.write("Finished processing %s files\n" % (file_num))

"""
Changelog:
28/10/14: Remove .csv extension (expected in input file)
29/10/14: Strips off any file extension, not specified any longer
          Now uses 'with open' statements, instead of opening and closing manually
15/01/15: Added an additional command line argument, '-s', that indicates comma
          separated values; if false, assume tabs or spaces.
"""

