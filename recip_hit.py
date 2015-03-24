#!/usr/bin/env python

"""
Changelog
---------
Author: Christen Klinger
Last Updated: February 12, 2015
"""

import argparse

parser = argparse.ArgumentParser(
    description = "Determines accessions for reciprocal best hits",
    epilog = """This program requires both forward and blast hit files
    in tab-delimited format with columns qacc sacc evalue as the first
    columns; it returns a csv file with one entry per line in the form
    'query, sacc, Fevalue, Revalue' such that the sacc entries may be
    extracted from the original database and used for downstream analysis
    of the reciprocal best hits.""")
parser.add_argument('-f', '--forward', help='forward BLAST results file')
parser.add_argument('-r', '--reverse', help='reverse BLAST results file')
parser.add_argument('-o', '--out', help='name of outfile')
args = parser.parse_args()

with open(args.forward, 'U') as i1:
    hit_dict = {}
    prev_line1 = ''
    for current_line1 in i1:
        #print "current line:" +  current_line1
        #print "previous line:" +  prev_line1
        current_list1 = current_line1.strip('\n').split('\t')
        try:
            prev_list1 = prev_line1.strip('\n').split('\t')
        except:
            pass
        if current_list1[0] == prev_list1[0] and current_list1[1] == prev_list1[1]:
            pass
        else:
            facc = current_list1[0]
            fhit = current_list1[1]
            feval = current_list1[2]

            if facc not in hit_dict.keys():
                hit_dict[facc] = []
                hit_dict[facc].append([fhit, feval])
            else:
                hit_dict[facc].append([fhit, feval])
        prev_line1 = current_line1

#print hit_dict
#print hit_dict.keys()

with open(args.reverse, 'U') as i2:
    recip_list = []
    prev_line2 = ''
    for current_line2 in i2:
        current_list2 = current_line2.strip('\n').split('\t')
        try:
            prev_list2 = prev_line2.strip('\n').split('\t')
        except:
            pass
        if current_list2[0] == prev_list2[0]:
            pass
        else:
            #print current_list2
            if current_list2[1] in hit_dict.keys():
                rhit = current_list2[0]
                qacc = current_list2[1]
                reval = current_list2[2]
                recip_list.append([rhit, qacc, reval])
        prev_line2 = current_line2

#print recip_list

outfile = str(args.out)

with open(outfile, 'w') as o:
    for query in hit_dict:
        for fhit, feval in hit_dict[query]:
            for rhit, qacc, reval in recip_list:
                if query == qacc and rhit == fhit:
                    o.write("%s,%s,%s,%s," % (query, fhit, feval, reval))
                    o.write('\n')




