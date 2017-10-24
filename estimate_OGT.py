#calculate predicted OGT according to Zeldovich
import sys
from Bio import SeqIO

num_ivywrel = 0
total_length = 0

proteins = SeqIO.parse(sys.argv[1], "fasta")
for record in proteins:
    seq = record.seq
    for char in seq:
        if char in 'IVYWREL':
            num_ivywrel += 1
        total_length += 1

f_ivywrel = float(num_ivywrel)/float(total_length)
print(f_ivywrel)
print("T_opt estimate according to Zeldovich: " + str(937.0*float(f_ivywrel) - 335.0))
