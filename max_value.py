#!/usr/bin/env python

TestDict = {'33066':[['240'],['122','347','121','347','PF00566.13','RabGAP-TBC','Family','2.4e-53']],
'76746':[['180'],['275','346','247','368','PF00566.13','RabGAP-TBC','Family','1.8e-10']],
'142360':[['400'],['59','144','58','152','PF00566.13','RabGAP-TBC','Family','1.6e-05']]}

def find_max_value(dict):
	maxvalue = ''
	for k in dict.keys():
		v1 = dict[k][0][0]
		if v1 > maxvalue:
			maxvalue = v1
		else:
			pass
	return maxvalue

maxval = find_max_value(TestDict)
print maxval

numkeys = len(TestDict.keys())
print numkeys