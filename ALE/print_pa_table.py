#for a directory of FASTA gene family files, compute a gene presence-absence (or Count-type) table
from __future__ import print_function
import os, re

to_check = [file for file in os.listdir("fasta/") if file.endswith(".fa")]
#first obtain a complete list of the species. This is an appalling inefficient "algorithm"
species = {}
for file in to_check:
    inh = open("fasta/" + file)
    for line in inh:
        if line.startswith(">"):
            fields = re.split("_", line[1:])
            sp = fields[0]
            species[sp] = 1

#...and now, read the sequence files one at a time and print out a line corresponding to the count profile

splist = species.keys()
print("Family\t", end = '')
for element in splist:
    print(element + "\t", end='')
print("\n", end = '')

for file in to_check:
    file_count = {}
    inh = open("fasta/" + file)
    for line in inh:
        fields = re.split("_", line[1:])
        if fields[0] in file_count:
            file_count[fields[0]] += 1
        else:
            file_count[fields[0]] = 1
    print(file + "\t", end = '')
    for sp in splist:
        if sp in file_count:
            print(str(file_count[sp]) + "\t", end = '')
        else:
            print("0\t", end = '')
    print("\n", end = '') 
