#!/usr/bin/env python


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

#print "GeneFam\tSupported_Hypothesis\tLikelihood\tDeltaSupport\tAlignment_Length\tSequences\tNum_Species\tDuplications\tTransfers\tLosses\tSpeciations"
print "GeneFam\tHypothesis\tLL"
to_do = [file for file in os.listdir(dirs[0] + "/") if file.endswith("rec")]
for file in to_do:
    have_them = check_have_reconciliations(file, dirs) 
    if have_them == 1:
        #this is a rec common to all species trees/hypotheses
        for hypothesis in dirs:
            lnl = extract_logl(hypothesis + "/" + file)
            print file + "\t" + hypothesis + "\t" + str(lnl)
