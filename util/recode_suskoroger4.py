#recode a FASTA alignment with saturation bins from Susko and Roger (2007)
#4 bins: AGNPST, CHWY, DEKQR, FILMV
#bin1 = list('AGNPST')
#print bin1
import sys
from Bio import AlignIO
alignment = AlignIO.read(open(sys.argv[1]), "fasta")
for record in alignment:
    seq = str(record.seq).upper()
    recoded_seq = ''
    for char in seq:
        if char == '-':
            recoded_seq += '-'
        elif char in list('AGNPST'):
            recoded_seq += 'A'
        elif char in list('CHWY'):
            recoded_seq += 'C'
        elif char in list('DEKQR'):
            recoded_seq += 'G'
        elif char in list('FILMV'):
            recoded_seq += 'T'
        elif char == 'X':
            recoded_seq += '-'
        else:
            print "Error: unrecognised aa in alignment: " + str(char)
            quit()
    print ">" + str(record.id) + "\n" + recoded_seq
