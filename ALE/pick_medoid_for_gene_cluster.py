#Pick a representative sequence for functional annotation of a cluster
from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio import AlignIO, SeqIO
import sys, os, re
from pprint import pprint

to_do = [file for file in os.listdir("fasta/") if file.endswith(".fa")]
for file in to_do:
    repseq = ''
    repfile = "medoid/" + file[:-3] + "_representative.fa"
    if os.path.exists(repfile):
        continue
    else:
        path = "fasta/" + file
        handle = open(path)
        seqs = SeqIO.to_dict(SeqIO.parse(handle, "fasta"))
        try:
            if len(seqs) > 2:
                alignment = "fasta/" + file[:-3] + ".aln"
                os.system("mafft --anysymbol fasta/" + file + " > " + alignment)
                if os.path.exists(alignment):
                    aln = AlignIO.read(alignment, "fasta")
                    calculator = DistanceCalculator('blosum62')
                    dm = calculator.get_distance(aln)
                    min_dist = 999999999.0
                    min_id = ''
                    #for record in seqs:
                        #find seq with shortest summed distance to all others

                    for i in range(len(dm.names)):
                        summed_dist = 0.0
                        for j in range(len(dm.names)): #self-dist is 0, so this loop should be fine
                            summed_dist += float(dm[i][j])
                        if summed_dist < min_dist:
                            min_dist = summed_dist
                            min_id = dm.names[i]
                    repseq = seqs[min_id]
                else:
                    repseq = seqs[seqs.keys()[0]]
            else:
                if len(seqs) == 1:
                    repseq = seqs[seqs.keys()[0]]
                else:
                #just pick the longest
                    len_seq1 = len(seqs[seqs.keys()[0]].seq)
                    len_seq2 = len(seqs[seqs.keys()[1]].seq)
                    if len_seq1 >= len_seq2:
                        repseq = seqs[seqs.keys()[0]]
                    else:
                        repseq = seqs[seqs.keys()[1]]
        except:
            repseq = seqs[seqs.keys()[0]]
        outh = open(repfile, "w")
        outh.write(">" + repseq.description + "\n" + str(repseq.seq))
        outh.close()
