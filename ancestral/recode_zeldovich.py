#recode a FASTA alignment into the Zeldovich categories: 0 (non-IVYWREL), 1 (IVYWREL) 
#bin1 = list('AGNPST')
#print bin1
import sys
from Bio import AlignIO
alignment = AlignIO.read(open(sys.argv[1]), "fasta")
alignment_length = alignment.get_alignment_length()
num_taxa = len(alignment)

print "#NEXUS"
print "begin data;"
print "\tdimensions ntax=" + str(num_taxa) + " nChar=" + str(alignment_length) + ";"
print "\tformat datatype=standard symbols=\"01\" gap=- missing=?;"
print "\tmatrix"

for record in alignment:
    seq = str(record.seq).upper()
    recoded_seq = ''
    for char in seq:
        if char == '-':
            recoded_seq += '-'
        elif char in list('IVYWREL'):
            recoded_seq += '1'
        else:
            recoded_seq += '0'
    print str(record.id) + "\t" + recoded_seq
print ";"
print "end;"
