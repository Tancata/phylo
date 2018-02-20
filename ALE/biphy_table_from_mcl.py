#for a MCL cluster file (out.seq.mci.*) compute a gene presence-absence (or Count-type) table
from __future__ import print_function
import os, re, sys

#to_check = [file for file in os.listdir("fasta/") if file.endswith(".fa")]
#first obtain a complete list of the species. This is an appalling inefficient "algorithm"
species = {}
#for file in to_check:
#    inh = open("fasta/" + file)
#    for line in inh:
#        if line.startswith(">"):
#            fields = re.split("_", line[1:])
#            sp = fields[0]
#            species[sp] = 1
with open(sys.argv[1]) as inh:
    for line in inh:
        members = re.split("\t", line.rstrip())
        for m in members:
            fields = re.split("_", m)
            sp = fields[0]
            species[sp] = 1
#...and now, read the sequence files one at a time and print out a line corresponding to the count profile

splist = species.keys()
print("Family\t", end = '')
for element in splist:
    print(element + "\t", end='')
print("\n", end = '')

with open(sys.argv[1]) as inh:
    for line in inh:
        family = {}
        mems = re.split("\t", line.rstrip())
        for m in mems:
            fields = re.split("_", m)
            if fields[0] in family:
                family[fields[0]] += 1
            else:
                family[fields[0]] = 1

        for sp in splist:
            if sp in family:
                print(str(family[sp]) + "\t", end = '')
            else:
                print("0\t", end = '')
print("\n", end = '') 
