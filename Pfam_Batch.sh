#!/bin/bash

# Runs batch PfamScan searches on a all .fa files in a directory
# Author: Christen Klinger
# Last modified: November 7, 2014

# sets query directory to current
QUERYDIR=`pwd`
# path to Pfam DBs
DB_DIR=/Users/cklinger/src/PfamScan/DB
# gets current date
now=$(date +"%Y%m%d")

QUERIES=`ls $QUERYDIR/*.fa`
echo "Using query files:"
echo "$QUERIES"

# make a separate directory for the output in the parent
#mkdir -p "$QUERYDIR/PfamScanOutput"

#OUTDIR="$QUERYDIR/PfamScanOutput"

for query in $QUERIES; do
	q_short_name=$(basename "$query")
	q_short_name="${q_short_name%.*}"

	pfam_scan.pl -fasta "$query" -dir "$DB_DIR" --outfile "${q_short_name}_${now}_PfamScan.txt" -e_dom 0.01 -e_seq 0.01
done

#EndScript

# Changelog:
# 20141107
# Added ability to output current date for output files
