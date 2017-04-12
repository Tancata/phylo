#simply add some tag to the fasta headers produced by prodigal to disambiguate protein sets from different isolates
#! /usr/bin/python

#Usage: add_id_to_fasta_header.py tag infile outfile
#OR:
#add_id_to_fasta_header.py infile outfile [tag is whatever comes before first . of infile)
import sys, re
tag = ''
infile = ''
outfile = ''

if len(sys.argv) == 4:
    tag = sys.argv[1]
    infile = open(sys.argv[2])
    outfile = sys.argv[3]
else:
    infile = open(sys.argv[1])
    outfile = sys.argv[2]
    bits = re.split("\.", sys.argv[1])
    tag = bits[0]

outh = open(outfile, "w")

for line in infile:
    if line.startswith(">"):
        modified_line = line.replace("(", "_").replace(")", "_").replace("|", "_").replace(':','_').replace(" ", "_")
        outh.write(">" + tag + "_" + modified_line[1:].rstrip() + "\n") 
    else:
        outh.write(line.rstrip() + "\n")
outh.close()
