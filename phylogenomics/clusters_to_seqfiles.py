#Read an MCL cluster file and a FASTA protein file and write FASTA output files corresponding to the clusters

import re, os, sys
from Bio import SeqIO

clustf = sys.argv[1]
fastaf = sys.argv[2]

seqs = SeqIO.index(fastaf, "fasta")
gid = 0
ch = open(clustf)
for line in ch:
    members = re.split("\t", line.rstrip())
    if len(members) > 3:
        gid += 1
        to_write = []
        for mem in members:
            to_write.append(seqs[mem])
        output_name = str(gid) + ".fa"
        oh = open(output_name, "w")
        SeqIO.write(to_write, oh, "fasta")
        oh.close()
