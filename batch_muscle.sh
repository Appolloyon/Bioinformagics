#!/bin/bash

# Runs batch muscle alignment on all .fa files in a directory
# Author: Christen Klinger
# Created: January 23, 2015
# Last Modified: 

# sets query directory to current
QUERYDIR=`pwd`

QUERIES=`ls $QUERYDIR/*.fa`
echo "Using query files:"
echo "$QUERIES"

for query in $QUERIES; do
    q_short_name=$(basename "$query")
    q_short_name="${q_short_name%.*}"

    muscle3.8.31_i86darwin64 -in "$query" -out "${q_short_name}.afa"
done

# EndScript

