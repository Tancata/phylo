#a method for ranking sites in an alignment according to GC bias, for filtering purposes. Inspired by the Munoz-Gomez et al. (2018) zed score for amino acid data
from Bio import SeqIO, AlignIO
import sys, operator
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

highGC = []
lowGC = []
ratios = {}
flat_ratios = []
flat_zeds = []
col_zed = {}

#find high and low GC taxa 
seqaln = SeqIO.index(sys.argv[1], "fasta")
scores_by_taxa = {}
for taxon in seqaln:
    gc = 0
    at = 0
    sequence = str(seqaln[taxon].seq)
    for char in sequence:
        if char in 'GC':
            gc += 1
        elif char in 'AT':
            at += 1
    ratio = float(gc)/float(at)
    scores_by_taxa[taxon] = ratio
    ratios[taxon] = ratio
    flat_ratios.append(ratio)
    if ratio > 1:
        highGC.append(taxon)
    else:
        lowGC.append(taxon)
#rank by ratio and print out list
sorted_taxa = sorted(ratios.items(), key=operator.itemgetter(1), reverse = True)
just_taxa = []
for taxon in sorted_taxa:
    print taxon[0] + "\t" + str(taxon[1])
    just_taxa.append(taxon[0])

#np_rat = np.array(flat_ratios)
#sns.distplot(np_rat)
#plt.show()

#now compute Z for each column in the alignment

alignment = AlignIO.read(sys.argv[1], "fasta")
for col in range(len(str(alignment[0].seq))):
    GARP_high = 0.0
    GARP_low = 0.0
    FIMNKY_high = 0.0
    FIMNKY_low = 0.0
    highGC_taxa = float(len(highGC))
    lowGC_taxa = float(len(lowGC))
    for rec in alignment:
        char = str(rec.seq)[col]
        if rec.id in highGC:
            if char in 'GC':
                GARP_high += 1.0/highGC_taxa
            elif char in 'AT':
                FIMNKY_high += 1.0/highGC_taxa
        elif rec.id in lowGC:
            if char in 'GC':
                GARP_low += 1.0/lowGC_taxa
            elif char in 'AT':
                FIMNKY_low += 1.0/lowGC_taxa
        else:
            print "Taxon " + str(rec.id) + " couldn't be assigned to high or low GC..."
            quit()

    zed = FIMNKY_low - FIMNKY_high + GARP_high - GARP_low
    flat_zeds.append(zed)
    print str(col) + "\t" + str(zed) + "\t" + str(FIMNKY_low) + "\t" + str(FIMNKY_high) + "\t" + str(GARP_high) + "\t" + str(GARP_low)
    print alignment[:, col]
    col_zed[col] = zed
#np_z = np.array(flat_zeds)
#sns.distplot(np_z)
#plt.show()

#now write alignments in which top X% of sites by zed have been removed - say 50% for now
sorted_zeds = sorted(col_zed.items(), key=operator.itemgetter(1))
num_cols = len(sorted_zeds)
cols_to_take = int(float(num_cols)/2.0)
print cols_to_take
selected_cols = []
for i in range(cols_to_take):
    selected_cols.append(sorted_zeds[i][0])
#    for rec in seqaln:
#        print rec + "\t" + str(seqaln[rec].seq)[i]
#print sites for most negative zeds

#print alignment[:, selected_cols[0]]

outfile = sys.argv[2]
outh = open(outfile, "w")
for rec in seqaln:
    seq_to_print = ''
    for col in selected_cols:
        seq_to_print += str(seqaln[rec].seq)[col]
    outh.write(">" + str(rec) + "\n" + str(seq_to_print) + "\n")
outh.close()
