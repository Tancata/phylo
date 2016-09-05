#!/usr/bin/env python

#given some species trees, and some gene families, compare the properties of gene families that support (have better likelihoods) one species tree over another.
#need a directory called "alignments" which contains the alignment files (some formatting conventions expected, e.g. ending in .phy, phylip-relaxed format, and that the ALE reconciliation files are 19 characters longer than the corresponding alignments. Prints out a dataframe for downstream analysis (e.g. with iPython, Pandas, etc)
#hypothesis, alignment_length, num_seqs, ds, ts, ls, speciations

from Bio import SeqIO, AlignIO, Phylo
import re, sys, os

dirs = sys.argv[1:]
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

print "GeneFam\tSupported_Hypothesis\tLikelihood\tDeltaSupport\tAlignment_Length\tSequences\tNum_Species\tDuplications\tTransfers\tLosses\tSpeciations"
to_do = [file for file in os.listdir(dirs[0] + "/") if file.endswith("rec")]
for file in to_do:
    have_them = check_have_reconciliations(file, dirs) 
    if have_them == 1:
        #this is a rec common to all species trees/hypotheses
        supported_hypothesis = ''
        value = 0.0
        delta = 0.0
        for hypothesis in dirs:
            lnl = extract_logl(hypothesis + "/" + file)
            #print hypothesis + "/" + file + "\t" + str(lnl) + "\t" + str(float(lnl))
            if value == 0.0: #first time
                supported_hypothesis = hypothesis
                value = float(lnl)
            elif value == float(lnl):
                supported_hypothesis = "No_lnl_difference"
            elif value < float(lnl):
                supported_hypothesis = hypothesis
                delta = float(lnl) - value #debug thing basically
                value = float(lnl)
            elif value > float(lnl):
                delta = value - float(lnl)

        path_hypothesis = supported_hypothesis
        if supported_hypothesis == "No_lnl_difference": #this code invalid for more than 2 hypotheses: BE CAREFUL and REMOVE in that case!
            path_hypothesis = dirs[0]

        #now calculate some properties of the gene family to compare among hypotheses
        aln = AlignIO.read(open("alignments/" + file[:-19]), "phylip-relaxed")
        aln_length = aln.get_alignment_length()
        num_seqs = len(aln)
        num_species = extract_species_num(path_hypothesis + "/" + file)
        dtls = extract_dtls(path_hypothesis + "/" + file) #obtain these estimates under the best supported hypothesis

        print file + "\t" + supported_hypothesis + "\t" + str(value) + "\t" + str(delta) + "\t" + str(aln_length) + "\t" + str(num_seqs) + "\t" + str(num_species) + "\t" + str(dtls[0]) + "\t" + str(dtls[1]) + "\t" + str(dtls[2]) + "\t" + str(dtls[3])
