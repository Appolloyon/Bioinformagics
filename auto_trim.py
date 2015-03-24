#!/usr/bin/env python

import re
import argparse

parser = argparse.ArgumentParser(
    description = "Trims masked nexus files",
    epilog = """This program takes masked nexus files and trims them
    based on either I or W mask lines""")
group = parser.add_mutually_exclusive_group()
group.add_argument('-i', '--inclusive', action='store_true')
group.add_argument('-w', '--exclusive', action='store_true')
parser.add_argument('infiles', nargs='+', help='list of infiles')
args = parser.parse_args()

for infile in args.infiles:
    outfile = infile.strip('_mask.nex')
    outfile = outfile + ('_trimmed.nex')

    sdict = {}
    index_list = []
    header = []
    footer = []
    with open(infile,'U') as i:
        linenum = 0
        for line in i:
            if linenum <= 17:
                header.append(line)
            elif linenum > 17:
                #print line
                last_line = 18
                if line == '\n':
                    break
                else:
                    try:
                        #print line
                        llist = line.strip('\n').split()
                        #print llist
                        sdict[llist[0]] = llist[1]
                        index_list.append(llist[0])
                    except:
                        pass
                    last_line += 1
            linenum += 1
        for line in i:
            if linenum > last_line:
                footer.append(line)
            linenum += 1

    #print sdict
    odict = {}
    for n in range(len(sdict['mask']) - 1):
        #print n
        if sdict['mask'][n] == 'I':
            #print str(sdict['mask'][n])
            for k,v in sdict.iteritems():
                if k not in odict.keys():
                    odict[k] = ''
                    odict[k] += v[n]
                else:
                    odict[k] += v[n]
            n += 1
        else:
            n += 1
    #print odict

    max_length = 0
    for i in index_list:
        if len(i) > max_length:
            max_length = len(i)

    nchar = len(odict['mask'])
    for i,e in enumerate(header):
        if re.search('NCHAR', e):
            rstring = '\t'+'DIMENSIONS'+'  '+'NCHAR='+str(nchar)+';'+'\n'
            header.pop(i)
            header.insert(i, rstring)

    with open(outfile,'w') as o:
        for e in header:
            o.write(e)
        for index in index_list:
            o.write('\t')
            o.write(index)
            o.write(' ' * ((max_length - len(index)) + 1))
            o.write(odict[index])
            o.write('\n')
        o.write('\n')
        for e in footer:
            o.write(e)
