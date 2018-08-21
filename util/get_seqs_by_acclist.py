#requires edirect to be installed
import re, sys, os
from Bio import SeqIO

to_get = []

inh = open(sys.argv[1])
for line in inh:
    if re.search("_", line.rstrip()):
        acc = line.rstrip() + ".1"
    else:
        acc = line.rstrip()
    to_get.append(acc)

for seq in to_get:
    tmpname = seq + ".tmp"
    os.system("esearch -db protein -query \"" + seq + " [ACCN]\" | efetch -format fasta > " + tmpname)
    print seq
