#give several sequence files as input. Outputs a single FASTA file containing the non-redundant sequences for all taxa, a file containing just the eukaryote sequences, and a file containing just the prokaryote species.
from __future__ import print_function
from Bio import SeqIO
import os, sys

def write_seq_file(filename, seqdict):
    outh = open(filename, "w")
    for element in seqdict:
        outh.write(">" + str(element) + "\n" + str(seqdict[element]) + "\n")
    outh.close()
    return

tag = sys.argv[1]
inputs = sys.argv[2:]
print(inputs)
seen_seqs = []
all = {}
eukaryotes = {}
prokaryotes = {}

euks = []
inh = open("eukaryotes_all3.txt")
for line in inh:
    euks.append(line.rstrip())
inh.close()

for file in inputs:
    seqz = SeqIO.index(file, "fasta")
    for record in seqz:
        sequence = seqz[record].seq
        if sequence in seen_seqs:
            continue
        else:
            seen_seqs.append(sequence)
            name = seqz[record].description
            if name in euks:
                all[name] = sequence
                eukaryotes[name] = sequence
            else:
                all[name] = sequence
                prokaryotes[name] = sequence

#print out the files
all_name = str(tag) + "_all.fa"
eukaryotes_name = str(tag) + "_eukaryotes.fa"
prokaryotes_name = str(tag) + "_prokaryotes.fa"

write_seq_file(all_name, all)
write_seq_file(eukaryotes_name, eukaryotes)
write_seq_file(prokaryotes_name, prokaryotes)

