#!/usr/bin/env python

#compare the results of dated and undated ALE reconciliations on the same gene set and (ultrametric) tree

#need a directory called "alignments" which contains the alignment files (some formatting conventions expected, e.g. ending in .phy, phylip-relaxed format, and that the ALE reconciliation files are 19 characters longer than the corresponding alignments. Prints out a dataframe for downstream analysis (e.g. with iPython, Pandas, etc)
#hypothesis, alignment_length, num_seqs, ds, ts, ls, speciations

from Bio import SeqIO, AlignIO, Phylo
import re, sys, os

def check_have_reconciliations(filename, dir_list): #given a reconciliation file (e.g. in the first directory, check whether the same gene family has also been reconciled in each of the other directories
    have_them = 1
    for dir in dir_list:
        if os.path.exists(dir + "/" + filename):
            continue
        else:
            have_them = 0
    return have_them

def extract_logl(rec_file):
    inh = open(rec_file)
    for line in inh:
        if line.startswith(">logl"):
            fields = re.split("\s+", line.rstrip())
            likelihood = fields[1]
    inh.close()
    return likelihood

def extract_dtls(rec_file): #extract the total number of inferred duplications, transfers, losses, and speciations from a reconciliation file
    inh = open(rec_file)
    dtls = []
    for line in inh:
        if line.startswith("Total"):
            fields = re.split("\s+", line.rstrip())
            dtls = [fields[1], fields[2], fields[3], fields[4]]
    inh.close()
    return dtls

def extract_species_num(rec_file):
    inh = open(rec_file)
    species_num = 0
    for line in inh:
        if line.startswith("S_terminal_branch"):
            fields = re.split("\s+", line.rstrip())
            if int(fields[-1]) > 0:
                species_num += 1
    return species_num

print "GeneFam\tReconciliationType\tLL\tDs\tTs\tLs\tSpecs"

dated_recs = [file for file in os.listdir(sys.argv[1]) if file.endswith(".ml_rec")]
undated_recs = [file for file in os.listdir(sys.argv[1]) if file.endswith(".uml_rec")]

for file in dated_recs:
    undated_equivalent = file[:-6] + "uml_rec"
    if undated_equivalent in undated_recs:
        #have a comparable dated and undated rec. Compare per-family LLs and total numbers of events.
        dated_lnl = extract_logl(sys.argv[1] + "/" + file)
        undated_lnl = extract_logl(sys.argv[1] + "/" + undated_equivalent)
        dated_dtls = extract_dtls(sys.argv[1] + "/" + file) #obtain these estimates under the best supported hypothesis
        undated_dtls = extract_dtls(sys.argv[1] + "/" + undated_equivalent) #obtain these estimates under the best supported hypothesis
        print file[:-7] + "\t" + "Dated" + "\t" + str(dated_lnl) + "\t" + str(dated_dtls[0]) + "\t" + str(dated_dtls[1]) + "\t" + str(dated_dtls[2]) + "\t" + str(dated_dtls[3])
        print file[:-7] + "\t" + "Undated" + "\t" + str(undated_lnl) + "\t" + str(undated_dtls[0]) + "\t" + str(undated_dtls[1]) + "\t" + str(undated_dtls[2]) + "\t" + str(undated_dtls[3])
