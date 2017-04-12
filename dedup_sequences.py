from Bio import SeqIO
import sys

seen_names = []

output_file = sys.argv[1] + "_dedup"
outh = open(output_file, "w")
for record in SeqIO.parse(sys.argv[1], "fasta"):
    if record.id in seen_names:
        continue
    else:
        seen_names.append(record.id)
        outh.write(">" + str(record.id) + "\n" + str(record.seq) + "\n")
outh.close()
