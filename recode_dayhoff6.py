#recode a FASTA alignment with 6-state Dayhoff
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
        elif char in list('AGPST'):
            recoded_seq += '1'
        elif char in list('DENQ'):
            recoded_seq += '2'
        elif char in list('HKR'):
            recoded_seq += '3'
        elif char in list('FYW'):
            recoded_seq += '4'
        elif char in list('ILMV'):
            recoded_seq += '5'
        elif char in list('C'):
            recoded_seq += '6'
        elif char == 'X':
            recoded_seq += '-'
        else:
            print "Error: unrecognised aa in alignment: " + str(char)
            quit()
    print ">" + str(record.id) + "\n" + recoded_seq
