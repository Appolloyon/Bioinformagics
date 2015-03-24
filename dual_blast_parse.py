#!/usr/bin/env python

import re
import os
import os.path
import sys

def ExtractAccession(QueryString): #removes just the accession from the hit column
	SearchStr1='\Agi.+'
	SearchStr2='\Ajgi.+'
	SearchStr3='\AsymbB.+'
	SearchStr4='\AContig.+'
	SearchStr5='\ATTHERM.+'
	SearchStr6='\AIMG.+'
	SearchStr7='\Atr.+'
	SearchStr8='\Aprei.+'
	SearchStr9='\Apult.+'
	SearchStr10='\Acrei.+'

	if re.search(SearchStr1, QueryString):
		try:
			StringList1 = QueryString.split('|')
			#print StringList1 #uncomment for debugging
			return StringList1[3]
		except AttributeError:
			return QueryString
	elif re.search(SearchStr2, QueryString):
		try:
			StringList2 = QueryString.split('|')
			#print StringList2
			return StringList2[2]
		except AttributeError:
			return QueryString
	elif re.search(SearchStr3, QueryString) or re.search(SearchStr4, QueryString):
		try:
			StringList3 = QueryString.split('|')
			#print StringList3
			return StringList3[0]
		except AttributeError:
			return QueryString
	elif re.search(SearchStr5, QueryString) or re.search(SearchStr6, QueryString):
		try:
			ResultStr='(\w+_\d+)#\w+'
			ResultSearch = re.search(ResultStr, QueryString)
			Result = ResultSearch.group(1)
			return Result
		except AttributeError:
			return QueryString
	elif re.search(SearchStr7, QueryString) or re.search(SearchStr8, QueryString)\
	or re.search(SearchStr9, QueryString) or re.search(SearchStr10, QueryString):
		try:
			StringList4 = QueryString.split('|')
			#print StringList4
			return StringList4[1]
		except:
			return QueryString
	else:
		return QueryString

Forward_Dir = (os.getcwd()+"/Forward")
Reverse_Dir = (os.getcwd()+"/Reverse")

FileList_Forward = [f for f in os.listdir(Forward_Dir) if \
os.path.isfile(os.path.join(Forward_Dir,f)) and f.endswith(".txt")]

FileList_Reverse = [f for f in os.listdir(Reverse_Dir) if \
os.path.isfile(os.path.join(Reverse_Dir,f)) and f.endswith(".txt")]

#print FileList_Forward
#print FileList_Reverse

#FileList_Forward = FileList_Forward.remove('.DS_Store')
#FileList_Reverse = FileList_Reverse.remove('.DS_Store')
#
#print FileList_Forward
#print FileList_Reverse


for File1 in FileList_Forward:
#	print File1
	for File2 in FileList_Reverse:
#		print File2
		pattern = (re.search('(\w+)_(\w+)_(\w+)_(.+)',File1).group(3))
		if re.search(pattern,File2):
#			print File2
			Out=pattern + "_out.csv"
#			print Out
#			with open(Out1,'w') as O1, open(Out2,'w') as O2:
			with open(os.path.join(Forward_Dir,File1), 'r') as f1:
				FList=[]
				prev_line1=''
				for current_line1 in f1:
#					print "Current:" + current_line1
#					print "Previous:" + prev_line1
					current_list1 = current_line1.strip('\n').split('\t')
					try:
						prev_list1 = prev_line1.strip('\n').split('\t')
					except(ValueError, TypeError, NameError):
						pass
					if (ExtractAccession(current_list1[0])==ExtractAccession(prev_list1[0]) \
					and ExtractAccession(current_list1[1])==ExtractAccession(prev_list1[1])):
						pass
					else:
						FAcc = ExtractAccession(current_list1[0])
						FHit = ExtractAccession(current_list1[1])
						FEvalue = float(current_list1[2])

						FList.append([FAcc,FHit,FEvalue])

					prev_line1 = current_line1
#				print FList

			with open(os.path.join(Reverse_Dir,File2), 'r') as f2:
					RDict={}
					AccList=[]
					prev_line2=''
					for current_line2 in f2:
#						print "Current:" + current_line2
#						print "Previous:" + prev_line2
						current_list2 = current_line2.strip('\n').split('\t')
						try:
							prev_list2 = prev_line2.strip('\n').split('\t')
						except(ValueError, TypeError, NameError):
							pass
						RAcc = ExtractAccession(current_list2[0])
						RHit = ExtractAccession(current_list2[1])
						REvalue = float(current_list2[2])
						if (ExtractAccession(current_list2[0])==ExtractAccession(prev_list2[0]) \
						and ExtractAccession(current_list2[1])==ExtractAccession(prev_list2[1])):
							pass
						else:
							if RAcc not in AccList:
								AccList.append(RAcc)
								RDict[RAcc]=[]
								RDict[RAcc] += [RHit,REvalue]
							else:
								RDict[RAcc] += [RHit,REvalue]
						prev_line2 = current_line2
#					print RDict

			with open(Out,'w') as O:
				for NP,PF,FE in FList:
					O.write("%s,%s,%s," % (NP,PF,FE,))
					for v in RDict.get(PF):
						O.write("%s," % (v))
					O.write('\n')


