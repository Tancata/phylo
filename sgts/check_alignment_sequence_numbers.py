#! /usr/bin/env python

#Just print a sorted list of sequence numbers per PHYLIP-formatted alignment/sequence file

from Bio import SeqIO
import os

seqs_per_fam = []

a = 0
b = 0
c = 0

decent_length = 0

alignments = [file for file in os.listdir(".") if file.endswith(".phy")]
for file in alignments:
    decent_length_thistime = 0
    num_seqs = 0
    handle = open(file, "rU")
    for record in SeqIO.parse(handle, "phylip-relaxed"):
        num_seqs += 1
        if len(str(record.seq)) >= 60:
            decent_length_thistime = 1
    seqs_per_fam.append(num_seqs)
    if decent_length_thistime == 1:
        decent_length += 1
    if num_seqs < 500:
        a += 1
    if num_seqs < 1000:
        b += 1
    if num_seqs < 300:
        c += 1
    if os.path.exists(file + ".ufboot"):
        continue
    else:
        if decent_length_thistime == 1 and num_seqs < 500:
            os.system("cp " + file + " " + "embryophyte_filtered_torun/" + file)
print seqs_per_fam.sort()
print len(seqs_per_fam)
print "<300: " + str(c)
print "<500: " + str(a)
print "<1000: " + str(b)
print "Decent length: " + str(decent_length)
