#!/usr/bin/env python

import os
import subprocess

fdir = os.getcwd() + '/Forward/'
rdir = os.getcwd() + '/Reverse/'

ffiles = [f for f in os.listdir(fdir) if os.path.isfile(os.path.join(fdir, f))]
rfiles = [f for f in os.listdir(rdir) if os.path.isfile(os.path.join(rdir, f))]

#for f in ffiles:
#    print f
#for r in rfiles:
#    print r

for f in ffiles:
    for r in rfiles:
        if f.split('_')[2] == r.split('_')[2]:
            outname = r.split('_')[0] + "_" + r.split('_')[2] + ".csv"
            subprocess.call(["recip_hit.py", "-f", os.path.join(fdir,f), "-r", os.path.join(rdir,r), "-o", outname])


