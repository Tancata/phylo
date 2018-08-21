from Bio import SeqIO
import sys

aln = SeqIO.index(sys.argv[1], "fasta")
num_tax = len(aln)
#num_char = len(str(aln[aln.keys()[0]].seq))
num_char = 73713
print "#NEXUS\nBegin data;\n\tDimensions ntax = " + str(num_tax) + " nchar = " + str(num_char) + ";\n\tFormat datatype = protein gap = -;\n\tMatrix\n"
for seq in aln:
    print aln[seq].description + "\t" + str(aln[seq].seq)
