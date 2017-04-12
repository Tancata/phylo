#!/usr/bin/env python
#subsample a tree by removing the sequences most distant from a target sequence, until a certain number of remaining sequences is reached
from Bio import Phylo, AlignIO, SeqIO
from collections import defaultdict
import sys, re
from operator import itemgetter

def calc_all_distances(t): #given a tree, return all pairwise summed branch length distances
    distances = defaultdict(dict)
    taxa = t.get_terminals()
    for i in range(len(taxa)-1):
        for j in range(i+1, len(taxa)):
            ij_dist = t.distance(taxa[i],taxa[j])
            distances[taxa[i].name][taxa[j].name] = ij_dist
            distances[taxa[j].name][taxa[i].name] = ij_dist
    return distances

def distance_to_target(taxon, t):
    distances = {}
    taxa = t.get_terminals()
    for sp in taxa:
        if sp.name == taxon.name:
            continue
        else:
            distances[sp] = t.distance(taxon, sp)
    return distances

def tree_distances(taxa, dists): #calculate summed-branch length distances for all pairs of taxa on a tree
    smallest_dist = float(9999999)
    taxon_to_drop = ''
    for i in range(len(taxa)-1):
        for j in range(i+1, len(taxa)):
            new_dist = dists[taxa[i].name][taxa[j].name]
            if new_dist < smallest_dist:
                if len(sys.argv) <= 3:
                    taxon_to_drop = taxa[i] #can setup a more complex selection here, e.g. if have genome size or completness, could drop the least complete
                else:
                    #drop taxon with greater number of gaps
                    if taxa[i].name in gaps and taxa[j].name in gaps:
                        gaps_i = gaps[taxa[i].name]
                        gaps_j = gaps[taxa[j].name]
                        if gaps_i > gaps_j:
                            taxon_to_drop = taxa[i]
                        else:
                            taxon_to_drop = taxa[j]
                    else:
                        if taxa[i].name not in gaps:
                            taxon_to_drop = taxa[i]
                        elif taxa[j].name not in gaps:
                            taxon_to_drop = taxa[j]
                smallest_dist = new_dist
    return taxon_to_drop

def count_gaps(aln):
    gapc = {}
    for record in aln:
        gapc[record.id] = int(record.seq.count("-"))
    return gapc 

#tree - first arg
#n - second arg
#alignment (or something else with which to calculate completeness)

if len(sys.argv) < 3:
    print "Usage: subsample_tree_by_distance_to_target.py NewickTreeFile NumToKeep targetID unaligned_fasta_file"
    quit()

treefile = sys.argv[1]
taxa_to_keep = int(sys.argv[2])
target_tag = sys.argv[3] #e.g. the gi number

tree = Phylo.read(sys.argv[1], "newick")
taxa = tree.get_terminals()

#all_distances = calc_all_distances(tree)
target_taxon = '' #the LGT candidate, against which all other sequences are assessed
for taxon in taxa:
    if re.search(target_tag, taxon.name):
        target_taxon = taxon

print target_taxon.name
distances = distance_to_target(target_taxon, tree)

#now drop seqs in order of decreasing distance from target, until desired number of sequences retained

num_taxa = len(taxa)
sorted_distances = sorted(distances.items(), key=itemgetter(1))
for i in range(taxa_to_keep,len(sorted_distances)):
    tree.prune(sorted_distances[i][0])

taxa = tree.get_terminals()
flat_taxa = []
for tip in taxa:
    flat_taxa.append(tip.name)
Phylo.draw_ascii(tree)

#print out the unaligned FASTA sequences for making the second tree
output_file = sys.argv[4] + "_reduced"
outh = open(output_file, "w")
fastah = SeqIO.parse(sys.argv[4], "fasta")
for seq in fastah:
    if seq.id in flat_taxa:  
        new_name = str(seq.description).replace('\t','_')
        new_name = new_name.replace(' ','_')
        outh.write(">" + new_name + "\n" + str(seq.seq) + "\n")
outh.close()
