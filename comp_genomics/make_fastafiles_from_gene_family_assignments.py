#take as input the output of "build_gene_fams_from_eggnogmapper_output.py", and create a FASTA file for each gene family.

from Bio import SeqIO
import os, sys, re

sequences = "all_ms_prots.fa" #set this to a FASTA file containing all sequences

all_seqs = SeqIO.index(sequences, "fasta")
gene_fams = {} #key = number, value = list of IDs


gene_fam_file = open("v") #set this to the output of the previous script
for line in gene_fam_file:
    fields = re.split("\t", line.rstrip())
    gene_fams[fields[0]].append(fields[1])

#now write a FASTA sequence file for each gene family
for fam in gene_fams.keys():
    output_filename = str(fam) + ".fasta"
    outh = open(output_filename, "w")
    for id in gene_fams[fam]:
        if id in all_seqs:
            #write it to the file
            outh.write(">" + all_seqs[id].description + "\n" + str(all_seqs[id].seq) + "\n")
        else:
            print "Uh oh! Sequence with ID " + str(id) + " is not in the all_seqs file!"
            quit()
    outh.close()
