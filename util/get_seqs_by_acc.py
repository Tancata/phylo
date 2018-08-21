#requires edirect to be installed
import re, sys, os
from Bio import SeqIO

seqs = SeqIO.index(sys.argv[1], "fasta")
for seq in seqs:
    bits = re.split("_", seq.rstrip())
    tmpname = bits[1] + ".tmp"
    os.system("esearch -db protein -query \"" + bits[1] + " [GI]\" | efetch -format fasta > " + tmpname)
    print bits[1]
