#!/usr/bin/env python

Usage="""

This program is the most recent version of the python-based script to retrieve
Fasta sequences automatically. It assumes a directory structure for genome
files with a top level, directories for each organisms named the same as the
files in the input stream (i.e. both files need at least one instance of the
same substring, e.g. for Homo sapiens, both should have 'Hsapiens' or 'Hsap'
or something along those lines). Within each of these directories, files should
be present for each genome, nucleotide files should have '_Genome' somewhere
in their name, and '_Prot' for protein files, and must be Fasta formatted.
Additionally, input files must contain one accession on each line.

Usage: Get_Any_Fasta.py {-P/-N} (files to parse)
-P specifies protein
-N specifies nucleotide
files to parse is a list of files, use Bash file globbing for many files

Note: this program requires BioPython to be installed.

Author: Christen Klinger
Last updated: August 25, 2014
"""

#change this to directory with genomes
dir_string="/Users/cklinger/Documents/Genomes_new_2014"

from Bio import SeqIO
import sys
import re
import os

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

if len(sys.argv) < 2:
    print Usage
    sys.exit(1)
else:
    file_list = sys.argv[2:]

if sys.argv[1] == "-P":
    search_str = "_Prot"
elif sys.argv[1] == "-N":
    search_str = "_Genome"
else:
    print "Please specify nucleotide or protein"
    sys.exit(1)

for infile in file_list:
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