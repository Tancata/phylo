#! /usr/bin/env python

#read a directory of *rec files and output a table of all the data for downstream analysis
#Usage: give directory containing rec files as first arg
import os, re, sys
from collections import defaultdict

print "GeneFamily\tBranch\tDs\tTs\tLs\tcopies"
to_do = [file for file in os.listdir(sys.argv[1]) if file.endswith(".uml_rec")]
for rec in to_do:
    inh = open(sys.argv[1] + rec)
    for line in inh:
        if re.match("S\_.+?branch", line):
            fields = re.split("\t", line.rstrip())
            print rec[:-8] + "\t" + fields[1] + "\t" + fields[2] + "\t" + fields[3] + "\t" + fields[4] + "\t" + fields[5]
