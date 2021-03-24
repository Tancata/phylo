#print a confidence set of gene family origination points based on LLs
from __future__ import division

import re, sys
from decimal import Decimal
import numpy as np

oriLL = {}
oriP = {}

total_probs = np.array([])

inh = open(sys.argv[1]) #uml_rec file
for line in inh:
    fields = re.split("\t", line.rstrip())
    if fields[0].startswith("S_"):
        oriLL[fields[1]] = float(fields[-1])
        oriP[fields[1]] = np.exp(Decimal(fields[-1])) 
        total_probs = np.append(total_probs, np.exp(Decimal(fields[-1])))
inh.close()

total = np.sum(total_probs)

for k in sorted(oriP, key=oriP.get, reverse=True):
    norm_prob = Decimal(oriP[k]) / total
    print(k + "\t" + str(oriP[k]) + "\t" + str(norm_prob))


