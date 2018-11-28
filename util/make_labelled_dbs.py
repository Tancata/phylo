#make a database of all protein sequences from a concatenate gene set, with each sequence labelled by its gene name/ID
#python(2) make_labelled_dbs.py file_extension concat_name output_file
import os, re, sys
from Bio import SeqIO

sg_extension = sys.argv[1] #the file extension of the single gene files
concat_name = sys.argv[2]
db_outfile = sys.argv[3]
outh = open(db_outfile, "w")
to_do = [file for file in os.listdir(".") if file.endswith(sg_extension)]
for file in to_do:
    gene_name_bits = re.split("\.", file)
    gene_id = gene_name_bits[0]
    gene_id_update = gene_id.replace("_","-") #want to parse on _ later, so clean these from gene names
    seqs = SeqIO.index(file, "fasta")
    for rec in seqs:
        outh.write(">" + concat_name + "_" + gene_id_update + "_" + seqs[rec].description + "\n" + str(seqs[rec].seq) + "\n")
outh.close()
