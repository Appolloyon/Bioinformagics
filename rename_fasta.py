#!/usr/bin/env python

import sys
from functions import filter_header, nonblank_lines

infiles = sys.argv[1:]

for infile in infiles:
    outfile = infile
    with open(infile, 'U') as i:
        lines = []
        for line in nonblank_lines(i):
            if line.startswith('>'):
                line = line.strip('>').strip('\n')
                #print line
                newline = filter_header(line)
                newline = '>' + newline
                lines.append(newline)
            else:
                line = line.strip('\n')
                lines.append(line)
    with open(outfile, 'w') as o:
        for line in lines:
            o.write(line + '\n')
