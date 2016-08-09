#! /usr/bin/env python

from Bio import SeqIO
import os, sys, re

# Process a directory of alignments. Create a new set of alignments in which only genes from a specific set of species are included.
# ./filter...py speciesList dirName outDirName

#Read in the list of species to keep. A bit of hard coding here to deal with the embryophyte case.

species = []
listf = open(sys.argv[1])
for line in listf:
    species.append(line.rstrip())
listf.close()

to_do = [file for file in os.listdir(sys.argv[2]) if file.endswith(".phy")]
for file in to_do:
    sequences_to_keep = []
    handle = open(sys.argv[2] + file, "rU")
    records = SeqIO.parse(handle, "phylip-relaxed")
    for rec in records:
        id_bits = re.split("_", rec.id)
        compound = id_bits[0] + id_bits[1]
        if id_bits[0] in species: #we want to keep this sequence
            sequences_to_keep.append(rec)
        elif compound in species:
            rec.id = compound + "_" + rec.id
            sequences_to_keep.append(rec)
    outfile = sys.argv[3] + "embryophytes_" + file
    if len(sequences_to_keep) >= 4:
        SeqIO.write(sequences_to_keep, outfile, "phylip-relaxed")
