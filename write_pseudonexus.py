from Bio import SeqIO
import sys

seqs = SeqIO.index(sys.argv[1], "fasta")
for seq in seqs:
	print seqs[seq].description + " " + str(seqs[seq].seq)
