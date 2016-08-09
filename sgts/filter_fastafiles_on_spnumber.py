from Bio import SeqIO
import os, re

to_include = [file for file in os.listdir(".") if file.endswith(".fa")]
for file in to_include:
    fam = {}
    #setup fam dict
    seqs = SeqIO.index(file, "fasta")
    for record in seqs:
        name_fields = re.split("_", seqs[record].id)
        species = name_fields[0]
        if species in fam:
            fam[species] += 1
        else:
            fam[species] = 1
    num_sp = len(fam.keys())
    if num_sp >= 2:
        os.system("cp " + file + " /media/tom/Data/future/arch_compgenomics/annotation/")

