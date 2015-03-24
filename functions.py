#!/usr/bin/env python

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

def get_fasta_file(subdir, search_str, dir_string):
    onlyfiles = [f for f in os.listdir(os.path.join(dir_string, subdir)) if\
    os.path.isfile(os.path.join(dir_string, subdir, f))]
    for f in onlyfiles:
        if re.search(search_str, f):
            fasta_file = os.path.join((os.path.join(dir_string, subdir)), f)
            return fasta_file

def split_input(string, chunk_size):
    num_chunks = len(string)/chunk_size
    if (len(string) % chunk_size != 0):
        num_chunks += 1
    output = []
    for i in range(0, num_chunks):
        output.append(string[chunk_size*i:chunk_size*(i+1)])
    return output

def nonblank_lines(f):
    for l in f:
        line = l.strip('\n')
        if line:
            yield line

def extractacc(qstring): #removes just the accession from the hit column
    sstring1='\Agi.+'
    sstring2='\Ajgi.+'
    sstring3='\AsymbB.+'
    sstring4='\AContig.+'
    sstring5='\ATTHERM.+'
    sstring6='\AIMG.+'
    sstring7='\Atr.+'
    sstring8='\Aprei.+'
    sstring9='\Apult.+'
    sstring10='\Acrei.+'

    if re.search(sstring1, qstring):
        try:
            slist1 = qstring.split('|')
            #print slist1 #uncomment for debugging
            return slist1[3]
        except AttributeError:
            return qstring
    elif re.search(sstring2, qstring):
        try:
            slist2 = qstring.split('|')
            #print sstring2
            return slist2[2]
        except AttributeError:
            return qstring
    elif re.search(sstring3, qstring) or re.search(sstring4, qstring):
        try:
            slist3 = qstring.split('|')
            #print StringList3
            return slist3[0]
        except AttributeError:
            return qstring
    elif re.search(sstring5, qstring) or re.search(sstring6, qstring):
        try:
            rstring='(\w+_\d+)#\w+'
            rsearch = re.search(rstring, qstring)
            return rsearch.group(1)
        except AttributeError:
            return qstring
    elif re.search(sstring7, qstring) or re.search(sstring8, qstring)\
	or re.search(sstring9, qstring) or re.search(sstring10, qstring):
        try:
            slist4 = qstring.split('|')
            #print StringList4
            return slist4[1]
        except:
            return qstring
    else:
        return qstring

def filter_header(qstring): #removes just the accession from the hit column
    sstring1='\Agi.+'
    sstring2='\Ajgi.+'
    sstring3='\AsymbB.+'
    sstring4='\AContig.+'
    sstring5='\ATTHERM.+'
    sstring6='\AIMG.+'
    sstring7='\Atr.+'
    sstring8='\Aprei.+'
    sstring9='\Apult.+'
    sstring10='\Acrei.+'
    sstring11='\ABBOV.+'
    sstring12='\AChro.+'
    sstring13='\Acgd.+'
    sstring14='\AEsi.+'
    sstring15='\ANCLIV.+'
    sstring16='\APF3D7.+'
    sstring17='\APVX.+'
    sstring18='\APYYM.+'
    sstring19='\ATGME49.+'
    sstring20='\ATP0.+'
    sstring21='\ACAMPEP.+'

    if re.search(sstring1, qstring):
		try:
			slist1 = qstring.split('|')
			#print slist1 #uncomment for debugging
			return slist1[3]
		except AttributeError:
			return qstring
    elif re.search(sstring2, qstring):
		try:
			slist2 = qstring.split('|')
			#print sstring2
			return slist2[2]
		except AttributeError:
			return qstring
    elif re.search(sstring3, qstring) or re.search(sstring4, qstring):
		try:
			slist3 = qstring.split('|')
			#print StringList3
			return slist3[0]
		except AttributeError:
			return qstring
    elif re.search(sstring5, qstring) or re.search(sstring6, qstring):
        try:
            slist4 = qstring.split('\t')
            return slist4[0]
        except AttributeError:
			return qstring
    elif re.search(sstring7, qstring) or re.search(sstring8, qstring)\
        or re.search(sstring9, qstring) or re.search(sstring10, qstring):
		try:
			slist5 = qstring.split('|')
			#print StringList4
			return slist5[1]
		except AttributeError:
			return qstring
    elif re.search(sstring11, qstring) or re.search(sstring12, qstring)\
        or re.search(sstring13, qstring) or re.search(sstring15, qstring)\
        or re.search(sstring16, qstring) or re.search(sstring17, qstring)\
        or re.search(sstring18, qstring) or re.search(sstring19, qstring)\
        or re.search(sstring20, qstring):
        try:
            slist6 = qstring.split('|')
            return slist6[0]
        except AttributeError:
            return qstring
    elif re.search(sstring14, qstring):
        try:
            slist7 = qstring.split()
            return slist7[0]
        except AttributeError:
            return qstring
    elif re.search(sstring21, qstring):
        try:
            slist8 = qstring.split()
            return slist8[0]
        except AttributeError:
            return qstring
    else:
        print 'no matches found'
        return qstring

