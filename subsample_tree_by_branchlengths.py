#!/usr/bin/env python
#given a tree and a number of taxa n, print the n taxa that maximize the representation of branch lengths on the tree. This is supposed to help with a question like "I want a subsampled representation of this 3,000 taxon tree which retains as much of the phylogenetic diversity as possible but contains only n taxa"
from Bio import Phylo, AlignIO
from collections import defaultdict
import sys

def calc_all_distances(t): #given a tree, return all pairwise summed branch length distances
    distances = defaultdict(dict)
    taxa = t.get_terminals()
    for i in range(len(taxa)-1):
        for j in range(i+1, len(taxa)):
            ij_dist = t.distance(taxa[i],taxa[j])
            distances[taxa[i].name][taxa[j].name] = ij_dist
            distances[taxa[j].name][taxa[i].name] = ij_dist
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
                    gaps_i = gaps[taxa[i].name]
                    gaps_j = gaps[taxa[j].name]
                    if gaps_i > gaps_j:
                        taxon_to_drop = taxa[i]
                    else:
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
    print "Usage: subsample_tree_by_branchlengths.py NewickTreeFile NumToKeep [optional: FastaAlignment]"
    quit()

treefile = sys.argv[1]
taxa_to_keep = int(sys.argv[2])

tree = Phylo.read(sys.argv[1], "newick")
taxa = tree.get_terminals()

gaps = {}
if len(sys.argv) > 3: #optional criterion to decide which taxon to drop, if supplied
    alignment = AlignIO.read(sys.argv[3], "fasta")
    gaps = count_gaps(alignment)

#calculate all distances, then drop taxa with the smallest distance repeatedly until remaining number of taxa is n.

all_distances = calc_all_distances(tree)
	
#now do recursive drop
num_taxa = len(taxa)
while num_taxa > taxa_to_keep:
    #get smallest distance, and drop one of the two taxa according to some other property, maybe
    print str(num_taxa)
    to_prune = tree_distances(taxa, all_distances)
    tree.prune(to_prune)
    taxa = tree.get_terminals()
    num_taxa = len(taxa)

for tip in taxa:
    print tip.name
Phylo.draw_ascii(tree)

aln_seqs = {} #totally unnecessary?
for record in alignment:
    aln_seqs[record.id] = str(record.seq)

if len(sys.argv) > 3:
    outh = open(sys.argv[3] + "_reduced.fasta", "w")
    for tip in taxa:
        outh.write(">" + str(tip.name) + "\n" + str(aln_seqs[tip.name]) + "\n")
    outh.close()
