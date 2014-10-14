#!/usr/bin/env python

class Seq():
	'Class string documentation'
	def __init__(self):
		pass

	def index(self):
		pass
	
	def lookup(self):
		pass

class Nuc_Seq(Seq):
	'Class string documentation'
	def __init__(self):
		pass

	pass

class Prot_Seq(Seq):
	'Class string documentation'
	def __init__(self):
		pass

	def check_codon(self):
		pass

	def update_codons(self):
		pass

"""
read in aligned nucleotide and protein seq files

parse each as per other programs 

write a loop to initialize a new object for each sequence with the first full
word of the description line as the var name and the sequence as one of the
object's attributes

now the actual program part:
for each object, get the current amino acid for the index value
check each one against each other, if all of them match, get the associated
	codon used, and then add it to the codon usage variable
advance the index for the nucleotide sequence three

if the amino acids do not match, advance the index for the nucleotide sequence
	only if the current value is not '-'

no matter what though, advance the amino acid sequence index forward one

continue on in this manner until the end of each sequence is reached

write output to a file which has the sequence ID and the associated list of 
	codons and the number of times they are used
""" 
