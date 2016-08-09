from Bio import SeqIO
import os, re, sys

outdir = sys.argv[1]

to_include = [file for file in os.listdir(".") if file.endswith(".phy")]
for file in to_include:
    fam = {}
    #setup fam dict
    handle = open (file, "rU")
    for record in SeqIO.parse(handle, "phylip-relaxed"):
        species = record.id #go on whole record
        if species in fam:
            fam[species] += 1
        else:
            fam[species] = 1
    num_sp = len(fam.keys())
    if num_sp >= 4:
        os.system("cp " + file + " " + outdir)

