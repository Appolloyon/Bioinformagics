#!/usr/bin/env python

"""
Changelog
---------
Author: Christen Klinger
Last updated: November 11, 2014
"""

#change this to directory with genomes
dir_string="/Users/cklinger/Documents/Genomes_new_2014"

import re
import os
import sys
import argparse

from Bio import SeqIO

parser = argparse.ArgumentParser(
    description = """Gets FASTA sequences for a list of accessions.""",
    epilog = """This program assumes a directory structure for genome
    files with a top level and directories for each organism named as
    per input files (i.e. both files need at least one instance of the
    same substring, e.g. Hsapiens or Hsap).  Within these directories
    nucleotide files should have '_Genome' somewhere in their name,
    and protein files '_Prot'.""")
group = parser.add_mutually_exclusive_group()
group.add_argument('-p', '--protein', action='store_true',
                    help='specify protein')
group.add_argument('-n', '--nucleotide', action='store_true',
                    help='specify nucleotide')
parser.add_argument('infiles', nargs='+', help='list of infiles')
args = parser.parse_args()

def determine_split(query_string):
    if re.search('|',query_string):
        return '|'
    else:
        return ''

def get_subdir_list(input_dir):
    subdir_list = [subdir for subdir in os.listdir(input_dir)]
    return subdir_list

def match_subdir(subdir_list, string):
    for subdir in subdir_list:
        if subdir in string:
            return subdir
        else:
            pass

def get_fasta_file(subdir, search_str):
    onlyfiles = [f for f in os.listdir(os.path.join(dir_string, subdir)) if\
    os.path.isfile(os.path.join(dir_string, subdir, f))]
    for f in onlyfiles:
        if re.search(search_str, f):
            fasta_file = os.path.join((os.path.join(dir_string, subdir)), f)
            return fasta_file

if args.protein:
    search_str = "_Prot"
elif args.nucleotide:
    search_str = "_Genome"

for infile in args.infiles:
    sys.stderr.write("Processing file {}\n".format(infile))
    outfile = infile.strip('.txt')
    outfile = outfile + "_Seqs.fa"

    fasta_file = get_fasta_file((match_subdir((get_subdir_list(dir_string)), infile)), search_str)

    with open(infile,'U') as f1, open(fasta_file,'U') as f2, open(outfile,'w') as o:
        wanted = set()
        for line in f1:
            line = line.strip()
            if line != "":
                wanted.add(line)

        for element in wanted:
            try:
                re.sub('\r', '', wanted)
            except(TypeError):
                pass

        fasta_sequences = SeqIO.parse(f2, 'fasta')

        for seq in fasta_sequences:
            new_header = seq.description.replace(" ", "|").replace("\t", "|")
            id_list = new_header.split(determine_split(seq.description))
            for element in id_list:
                if element in wanted:
                    SeqIO.write([seq], o, "fasta")

"""
Changelog:
August 25, 2014:
-changed the definition of get_fasta_file to consider only files
"""
