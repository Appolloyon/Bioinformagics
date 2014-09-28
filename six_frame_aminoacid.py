#!/usr/bin/env python

import re
import sys

def split_input(string, chunk_size):
    """splits a string into a number of chunks of max length chunk_size"""
    num_chunks = len(string)/chunk_size
    if (len(string) % chunk_size != 0):
        num_chunks += 1
    output = []
    for i in range(0, num_chunks):
        output.append(string[chunk_size*i:chunk_size*(i+1)])
    return output

def translate(string):
    """translates a given nucleotide sequence into protein"""

